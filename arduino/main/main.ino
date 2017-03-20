#define VITESSE 340000 //vitesse du son 340000 mm/s

const int USTrig = 8; // Déclencheur sur la broche 8
const int USEcho = 9; // Réception sur la broche 9
const int led = 2; // LED sur la broche 2 

String command = "";
boolean commandComplete = false;
boolean isSent = false;

void setup() {
    Serial.begin(9600);
    pinMode(led, OUTPUT);
    digitalWrite(led, HIGH);
    
    command.reserve(200);
    setupWaterLevel();
}

void loop() {
  if (checkSending()) {
    // Send values
    readWaterLevel();
  }

  if (commandComplete) {
    checkCommand(command);
    
    // Clear the command:
    command = "";
    commandComplete = false;
  }
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
  if ((millis() % 1000) < 500) {
    if (!isSent) {
      isSent = true;
      return true;
    }
  } else {
    isSent = false;
  }

  return false;
}

void checkCommand(String command) {
  Serial.print(command);
  if (command.startsWith("PUMP_IN=0")) {
    Serial.println("LED OFF");
    digitalWrite(led, HIGH);
  } else if (command.startsWith("PUMP_IN=1")) {
    Serial.println("LED ON");
    digitalWrite(led, LOW);
  }
}

void setupWaterLevel() {
  pinMode(USTrig, OUTPUT);
  pinMode(USEcho, INPUT);
  
  digitalWrite(USTrig, LOW);
}

void readWaterLevel() {
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
    Serial.println(distance); //affiche la distance mesurée (en mètres)
  }
}

