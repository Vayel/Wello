#define VITESSE 340000 //vitesse du son 340000 mm/s

const int USTrig = 8; // Déclencheur sur la broche 8
const int USEcho = 9; // Réception sur la broche 9
const int led = 7; // LED sur la broche 7 
const int warningButton = 3; // Bouton d'arrêt d'urgence sur la broche 3
const int flowmeter = 2; // Flowmeter sur la broche 2
const int pump = 10; // Pump sur la broche 10 (CH1)

String command = "";
boolean commandComplete = false;
unsigned long currentTime;
unsigned long previousTime;

// Flowmeter variables
volatile int  flowmeterCounter;     // Measures flow meter pulses
unsigned int  flowmeterResult;      // Calculated litres/hour
unsigned long beginFlowmeterDate;   // Begin date

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

  // Pump
  setupWarningButton();

  Serial.println("PUMP_IN=0");
}

void loop() {
  // Send values
  if (checkSending()) {
    readFlowmeter();
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

void setupFlowmeter() {
  pinMode(flowmeter, INPUT);
  attachInterrupt(0, increaseFlowmeterCounter, RISING); // Setup Interrupt
  sei();                                             // Enable interrupts
}

void increaseFlowmeterCounter()
{ 
   flowmeterCounter++;
} 

void readFlowmeter() {
  // Every second, calculate and print litres/hour
  // Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min. (Results in +/- 3% range)
  flowmeterResult = (flowmeterCounter * 60 / 7.5); // (Pulse frequency x 60 min) / 7.5Q = flow rate in L/hour 
  flowmeterCounter = 0;                   // Reset Counter

  Serial.print("WATER_FLOW_IN=");
  Serial.println(flowmeterResult, DEC);
}

void setupPump() {
  pinMode(pump, OUTPUT);
}

void warningButtonAction() {
  //Serial.println("ARRETTTTTTTTTTTTTTTTTTTTTTT DURGENCEEEEEE");
}

void setupWarningButton() {
  pinMode(warningButton, INPUT);
  attachInterrupt(1, warningButtonAction, FALLING); // Setup Interrupt
  sei();                                             // Enable interrupts
}

