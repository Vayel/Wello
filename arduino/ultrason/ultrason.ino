#define VITESSE 340 //vitesse du son 340 m/s

const int USTrig = 8; // Déclencheur sur la broche 8
const int USEcho = 9; // Réception sur la broche 9

void setup() {
    pinMode(USTrig, OUTPUT);
    pinMode(USEcho, INPUT);

    digitalWrite(USTrig, LOW);

    Serial.begin(9600);
}

void loop() {
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
      Serial.println("Onde perdue, mesure échouée !");
   }
   else
   {
      // 4. On divise cette durée par deux pour n'avoir qu'un trajet
      duree = duree/2;

      // 5. On calcule la distance avec la formule d=v*t
      float temps = duree/1000000.0; //on met en secondes
      float distance = temps*VITESSE; //on multiplie par la vitesse, d=t*v

      // 6. On affiche la distance
      Serial.print("Duree = ");
      Serial.println(temps); //affiche le temps de vol d'un trajet en secondes
      Serial.print("Distance = ");
      Serial.println(distance); //affiche la distance mesurée (en mètres)
   }

   // petite pause
   delay(250);

}
