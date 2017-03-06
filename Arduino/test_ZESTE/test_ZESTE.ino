void setup()
{
    Serial.begin(9600);
}

void loop()
{
    // variable contenant le caractère à lire
    char carlu = 0;
    // variable contenant le nombre de caractère disponibles dans le buffer
    int cardispo = 0;

    cardispo = Serial.available();

    while(cardispo > 0) // tant qu'il y a des caractères à lire
    {
        carlu = Serial.read(); // on lit le caractère
        Serial.print(carlu); // puis on le renvoi à l’expéditeur tel quel
        cardispo = Serial.available(); // on relit le nombre de caractères dispo
        Serial.print(cardispo);
    }
    // fin du programme
}
