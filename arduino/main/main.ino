#define VITESSE 340000 //vitesse du son 340000 mm/s

const int USTrig = 8; // Déclencheur sur la broche 8
const int USEcho = 9; // Réception sur la broche 9
const int led = 7; // LED sur la broche 7
const int flowmeterIn = 3; // Flowmeter In sur la broche 3
const int flowmeterOut = 2; // Flowmeter Out sur la broche 3
const int pump = 10; // Pump sur la broche 10 (CH1)
const int electrovanne = 11; // Electrovanne sur la broche 11 (CH2)
const int urbanNetwork = 12;

String command = "";
boolean commandComplete = false;
unsigned long currentTime;
unsigned long previousTime;

// Flowmeter variables
volatile int  flowmeterInCounter;     // Measures flow meter pulses
unsigned int  flowmeterInResult;      // Calculated litres/hour
volatile int  flowmeterOutCounter;     // Measures flow meter pulses
unsigned int  flowmeterOutResult;      // Calculated litres/hour

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);

  currentTime = millis();
  previousTime = currentTime;
  
  // Flowmeter 1
  setupFlowmeter();

  // WaterDistance
  setupWaterDistance();

  // Pump
  setupPump();

  // Electrovanne
  setupElectrovanne();

  setupUrbanNetwork();
}

void loop() {
  // Send values
  if (checkSending()) {
    readFlowmeterIn();
    readFlowmeterOut();
    readWaterDistance();
  }

  // Receive commands
  if (commandComplete) {
    checkReceiving(command);
    
    // Clear the command:
    command = "";
    commandComplete = false;
  }

  // Update current time
  currentTime = millis();
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    command += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      commandComplete = true;
    }
  }
}

boolean checkSending() {
  if (currentTime >= (previousTime + 1000)) {
    previousTime = currentTime;              // Updates previousTime
    return true;
  }

  return false;
}

void checkReceiving(String command) {
  if (command.startsWith("PUMP_IN=0")) {
    Serial.println("PUMP_IN=0");
    digitalWrite(pump, LOW);
  } else if (command.startsWith("PUMP_IN=1")) {
    Serial.println("PUMP_IN=1");
    digitalWrite(pump, HIGH);
  } else if (command.startsWith("URBAN_NETWORK=0")) {
    Serial.println("URBAN_NETWORK=0");
    digitalWrite(urbanNetwork, HIGH);
  } else if (command.startsWith("URBAN_NETWORK=1")) {
    Serial.println("URBAN_NETWORK=1");
    digitalWrite(urbanNetwork, LOW);
  } else if (command.startsWith("ELECTROVANNE=0")) {
    Serial.println("ELECTROVANNE=0");
    digitalWrite(electrovanne, LOW);
  } else if (command.startsWith("ELECTROVANNE=1")) {
    Serial.println("ELECTROVANNE=1");
    digitalWrite(electrovanne, HIGH);
  }
}

void setupWaterDistance() {
  pinMode(USTrig, OUTPUT);
  pinMode(USEcho, INPUT);
  
  digitalWrite(USTrig, LOW);
}

void readWaterDistance() {
  // 1. Un état haut de 10 microsecondes est mis sur la broche "Trig"
  digitalWrite(USTrig, HIGH);
  delayMicroseconds(10); //on attend 10 µs
  // 2. On remet à l’état bas la broche Trig
  digitalWrite(USTrig, LOW);
  
  // 3. On lit la durée d’état haut sur la broche "Echo"
  unsigned long duree = pulseIn(USEcho, HIGH);
  
  if(duree > 30000)
  {
    // si la durée est supérieure à 30ms, l'onde est perdue
    //Serial.println("Onde perdue, mesure échouée !");
  }
  else
  {
    // 4. On divise cette durée par deux pour n'avoir qu'un trajet
    duree = duree/2;
  
    // 5. On calcule la distance avec la formule d=v*t
    float temps = duree/1000000.0; //on met en secondes
    long distance = long(temps*VITESSE); //on multiplie par la vitesse, d=t*v
  
    // 6. On affiche la distance
    Serial.print("WATER_DISTANCE=");
    Serial.println(distance); //affiche la distance mesurée (en mètres)

    // 7. Marge de sécurité
    if (distance <= 50 && digitalRead(pump) == HIGH) {
      digitalWrite(pump, LOW);
    }
  }
}

void setupPump() {
  pinMode(pump, OUTPUT);
  digitalWrite(pump, LOW);
  Serial.println("PUMP_IN=0");
}

void setupElectrovanne() {
  pinMode(electrovanne, OUTPUT);
  digitalWrite(electrovanne, LOW);
  Serial.println("ELECTROVANNE=0");
}

void setupUrbanNetwork() {
  pinMode(urbanNetwork, OUTPUT);
  digitalWrite(urbanNetwork, HIGH);
  Serial.println("URBAN_NETWORK=0");
}

void setupFlowmeter() {
  pinMode(flowmeterIn, INPUT);
  pinMode(flowmeterOut, INPUT);
  attachInterrupt(digitalPinToInterrupt(flowmeterIn), increaseFlowmeterInCounter, RISING); // Setup Interrupt
  attachInterrupt(digitalPinToInterrupt(flowmeterOut), increaseFlowmeterOutCounter, RISING); // Setup Interrupt
  sei();                                             // Enable interrupts
}

void increaseFlowmeterInCounter()
{ 
   flowmeterInCounter++;
} 

void increaseFlowmeterOutCounter()
{ 
   flowmeterOutCounter++;
} 

void readFlowmeterIn() {
  // Every second, calculate and print litres/hour
  // Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min. (Results in +/- 3% range)
  flowmeterInResult = (flowmeterInCounter * 60 / 7.5); // (Pulse frequency x 60 min) / 7.5Q = flow rate in L/hour 
  flowmeterInCounter = 0;                   // Reset Counter

  Serial.print("WATER_FLOW_IN=");
  Serial.println(flowmeterInResult, DEC);
}

void readFlowmeterOut() {
  // Every second, calculate and print litres/hour
  // Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min. (Results in +/- 3% range)
  flowmeterOutResult = (flowmeterOutCounter * 60 / 7.5); // (Pulse frequency x 60 min) / 7.5Q = flow rate in L/hour 
  flowmeterOutCounter = 0;                   // Reset Counter

  Serial.print("WATER_FLOW_OUT=");
  Serial.println(flowmeterOutResult, DEC);
}

