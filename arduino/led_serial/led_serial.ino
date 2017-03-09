const int maLed = 11; // on met une LED sur la broche 2
// variable contenant le caractère à lire

void setup()
{
    pinMode(maLed, OUTPUT);
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
        analogWrite(maLed, 10);
      } else if (value.equals("off")) {
        analogWrite(maLed, 0);
      }
    }
}
