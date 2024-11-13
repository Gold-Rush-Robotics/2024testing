const int sensorPin1 = A1;
const int sensorPin2 = A2;
const int sensorPin3 = A3;
const int infraredPin = A0;
int hallTrigger = 800;
int IRTrigger = 100;
int sensorValue1 = 0;
int sensorValue2 = 0;
int sensorValue3 = 0;
int IRValue = 0;

bool objectDetected () {
  return (IRValue < IRTrigger);
}

bool magnetDetected () {
  return (sensorValue1 < hallTrigger || sensorValue2 < hallTrigger || sensorValue3 < hallTrigger);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);      // Start serial communication at 9600 bps
  pinMode(sensorPin1, INPUT); // Set the sensor pin as input
  pinMode(sensorPin2, INPUT); // Set the sensor pin as input
  pinMode(sensorPin3, INPUT); // Set the sensor pin as input
  pinMode(infraredPin, INPUT);
}

void loop() {
  
  // read in sensor values
  sensorValue1 = analogRead(sensorPin1);
  sensorValue2 = analogRead(sensorPin2);
  sensorValue3 = analogRead(sensorPin3);
  IRValue = analogRead(infraredPin);

  Serial.println(sensorValue1);
  // logic
  /*
  if (objectDetected()) {
  if (magnetDetected()) Serial.println("geodynium detected");
    else Serial.println("nebulite detected");
  }
  */
  if (magnetDetected()) Serial.println("geodynium detected");

  // Add a small delay to avoid flooding the Serial Monitor
  delay(1000);  // Delay for 100 milliseconds (0.1 seconds)
}
