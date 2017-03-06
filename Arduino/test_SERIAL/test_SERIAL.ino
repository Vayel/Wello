const int maLed = 2; // on met une LED sur la broche 2
// variable contenant le caractère à lire

void setup()
{
    pinMode(maLed, OUTPUT); // la LED est une sortie
    digitalWrite(maLed, HIGH); // on éteint la LED
    Serial.begin(9600); // on démarre la voie série
    Serial.println("Démarrage");
    Serial.setTimeout(10);
}

void loop()
{
    // Chaine de caractères
    String value = "";

    if (Serial.available() > 0) // tant qu'il y a des caractères à lire
    {
        value = Serial.readString();
    }

    if (!value.equals("")) {
      Serial.println(value);

      if (value.equals("on")) {
        Serial.println("LED ON");
        digitalWrite(maLed, LOW);
      } else if (value.equals("off")) {
        Serial.println("LED OFF");
        digitalWrite(maLed, HIGH);
      }
    }
}
