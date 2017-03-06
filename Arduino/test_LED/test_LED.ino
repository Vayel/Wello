const int led_rouge = 2;   // définition de la broche 2 de la carte en tant que variable

void setup() {
  // initialisation de la broche 2 comme étant une sortie
  pinMode(led_rouge, OUTPUT);
}

void loop() {
  digitalWrite(led_rouge, LOW);
  delay(1000);
  digitalWrite(led_rouge, HIGH);
  delay(1000);
}
