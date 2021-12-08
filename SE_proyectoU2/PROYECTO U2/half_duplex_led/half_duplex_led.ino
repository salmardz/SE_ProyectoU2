int sensor1 = A0;
int sensor2 = A1;
int sensor3 = A2;

int ledAccion1 = 12;
int ledAccion2 = 11;
int ledAccion3 = 10;

void setup() {
  pinMode(ledAccion1, OUTPUT);
   pinMode(ledAccion2, OUTPUT);
  pinMode(ledAccion3, OUTPUT);


  Serial.begin(9600);
  Serial.setTimeout(100);
}

int valor1;
int valor2;
int valor3;

int accion;
void loop() {

  //if (Serial.available() > 0) {
    //accion = Serial.readString().toInt(); //0 o 1
    //digitalWrite(ledAccion, accion);
 // }
 
  if (Serial.available ()>0){
    accion = Serial.readString().toInt();
    if (accion =='1'){
      digitalWrite(ledAccion1, HIGH);
     // digitalWrite(ledAccion1, accion);
    }
  }
  if (Serial.available ()>0){
    accion = Serial.readString().toInt();
    if (accion =='2'){
      //digitalWrite(ledAccion2, HIGH);
      digitalWrite(ledAccion2, accion);
    }
  }
    if (Serial.available ()>0){
    accion = Serial.readString().toInt();
    if (accion =='3'){
      //digitalWrite(ledAccion3, HIGH);
      digitalWrite(ledAccion3, accion);
    }
  }
  


  valor1 = analogRead(sensor1);
  valor2 = analogRead(sensor2);
  valor3 = analogRead(sensor3);


  valor1 = map(valor1, 0, 1023, 0, 100);
  valor2 = map(valor2, 0, 1023, 0, 100);
  valor3 = map(valor3, 0, 1023, 0, 100);

  Serial.println("I" + String(valor1) + "R" + String(valor2) + "R" + String(valor3) + "F");

  delay(100);
}
