const int unBouton = 2;   // un bouton sur la broche 2
const int led_rouge = 4;  // définition de la broche 4 de la carte en tant que variable
int val = 0;

void on() {
  digitalWrite(led_rouge, LOW);
  Serial.println("ON");
}

void off() {
  digitalWrite(led_rouge, HIGH);
  Serial.println("OFF");
}

void setup()
{
    // on met le bouton en entrée
    pinMode(unBouton, INPUT);
    pinMode(led_rouge, OUTPUT);
    // on active la résistance de pull-up en mettant la broche à l'état haut
    // (mais cela reste toujours une entrée)
    digitalWrite(unBouton, HIGH);
    Serial.begin(9600);
    attachInterrupt(digitalPinToInterrupt(unBouton), on, CHANGE);
    attachInterrupt(digitalPinToInterrupt(unBouton), off, HIGH);
}

void loop()
{
  /*Serial.println(digitalRead(unBouton));
  if (digitalRead(unBouton) == LOW) {
    digitalWrite(led_rouge, LOW);
    Serial.println("ON");
  } else {
    digitalWrite(led_rouge, HIGH);
    Serial.println("OFF");
  }*/
}

