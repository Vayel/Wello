#include <Controllino.h>
#include <Ethernet.h> // Make sure to use Controllino's Ethernet module (see compilation logs)
#include <WebServer.h> // https://github.com/sirleech/Webduino

/*
 * Ethernet config
 */

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 167, 100);
WebServer webserver("", 80);

#define STATE_POST_PARAM_NAME "state"
#define POST_PARAM_NAME_LEN 32
#define POST_PARAM_VALUE_LEN 5
#define INVALID_STATE -1

/*
 * Pins config
 */

#define PUMP_IN CONTROLLINO_D0
#define URBAN_NETWORK CONTROLLINO_D1
// TODO
#define FLOWMETER_IN 4
#define FLOWMETER_OUT 5

#define ON 1
#define OFF 0

volatile int flowmeterInPulses;
volatile int flowmeterOutPulses;

/*
 * Custom methods
 */

void commandRelay(int pin, bool on) {
  if (on) {
    digitalWrite(pin, HIGH);
  } else {
    digitalWrite(pin, LOW);
  }
}

void commandPumpIn(bool on) {
  commandRelay(PUMP_IN, on);
}

void commandUrbanNetwork(bool on) {
  commandRelay(URBAN_NETWORK, on);
}

void receiveFlowmeterInPulse() { 
   flowmeterInPulses++;
} 

void receiveFlowmeterOutPulse() { 
   flowmeterOutPulses++;
} 

/*
 * HTTP routes
 */
void home(WebServer &server, WebServer::ConnectionType type, char *, bool) {
  server.println("HTTP/1.1 200 OK");
  server.println("Content-Type: application/json");
  server.println();
  server.println("{");

  server.print("\"pump_in\": ");
  server.print(digitalRead(PUMP_IN) ? "1" : "0");
  server.println(",");

  server.print("\"urban_network\": ");
  server.print(digitalRead(URBAN_NETWORK) ? "1" : "0");
  server.println(",");

  server.print("\"water_distance\": ");
  server.print("0"); // TODO
  server.println(",");

  server.print("\"flow_in\": ");
  server.print("0"); // TODO
  server.println(",");

  server.print("\"flow_out\": ");
  server.println("0"); // TODO

  server.println("}");
}

void readOutputState(WebServer &server, int pin) {
  if (digitalRead(pin)) {
    P(msg) = "1";
    server.printP(msg);
  } else {
    P(msg) = "0";
    server.printP(msg);
  }
}

int readStatePostParam(WebServer &server) {
  char name[POST_PARAM_NAME_LEN];
  char value[POST_PARAM_VALUE_LEN];
  while (server.readPOSTparam(name, POST_PARAM_NAME_LEN, value, POST_PARAM_VALUE_LEN)) {
    if (strcmp(name, STATE_POST_PARAM_NAME) == 0) {
      break;
    }
  }
  if (strcmp(name, STATE_POST_PARAM_NAME) == 0) return strcmp(value, "0") == 0 ? OFF : ON;
  return INVALID_STATE;
}

void pumpInRoute(WebServer &server, WebServer::ConnectionType type, char *, bool) {
  server.httpSuccess();
  if (type == WebServer::GET) {
    readOutputState(server, PUMP_IN);
  } else if (type == WebServer::POST) {
    int state = readStatePostParam(server);
    if (state != INVALID_STATE) commandPumpIn(state);
  }
}

void urbanNetworkRoute(WebServer &server, WebServer::ConnectionType type, char *, bool) {
  server.httpSuccess();
  if (type == WebServer::GET) {
    readOutputState(server, URBAN_NETWORK);
  } else if (type == WebServer::POST) {
    int state = readStatePostParam(server);
    if (state != INVALID_STATE) commandUrbanNetwork(state);
  }
}

void flowInRoute(WebServer &server, WebServer::ConnectionType type, char *, bool) {
  server.httpSuccess();
  if (type == WebServer::GET) {
    P(msg) = "0"; // TODO
    server.printP(msg);
  }
}

void flowOutRoute(WebServer &server, WebServer::ConnectionType type, char *, bool) {
  server.httpSuccess();
  if (type == WebServer::GET) {
    P(msg) = "0"; // TODO
    server.printP(msg);
  }
}

void waterDistanceRoute(WebServer &server, WebServer::ConnectionType type, char *, bool) {
  server.httpSuccess();
  if (type == WebServer::GET) {
    P(msg) = "0"; // TODO
    server.printP(msg);
  }
}

/*
 * Arduino methods
 */
void setup() {
  pinMode(PUMP_IN, OUTPUT);
  pinMode(URBAN_NETWORK, OUTPUT);
  pinMode(FLOWMETER_IN, INPUT);
  pinMode(FLOWMETER_OUT, INPUT);

  commandPumpIn(OFF);
  commandUrbanNetwork(OFF);

  attachInterrupt(digitalPinToInterrupt(FLOWMETER_IN), receiveFlowmeterInPulse, RISING);
  attachInterrupt(digitalPinToInterrupt(FLOWMETER_OUT), receiveFlowmeterOutPulse, RISING);
  
  sei(); // Enable interrupts

  Ethernet.begin(mac, ip);
  webserver.setDefaultCommand(&home);
  webserver.addCommand("pump_in", &pumpInRoute);
  webserver.addCommand("urban_network", &urbanNetworkRoute);
  webserver.addCommand("flow_in", &flowInRoute);
  webserver.addCommand("flow_out", &flowOutRoute);
  webserver.addCommand("water_distance", &waterDistanceRoute);
  webserver.begin();
}

void loop() {
  char buff[64];
  int len = 64;
  webserver.processConnection(buff, &len);
}
