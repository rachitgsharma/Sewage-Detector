#include <BluetoothSerial.h>
#include <NewPing.h>

BluetoothSerial SerialBT;

const int triggerPin = 13; // HC-SR04 trigger pin
const int echoPin = 12;    // HC-SR04 echo pin
const int limitSwitchPin = 14; // Limit switch input pin

void setup() {
  Serial.begin(115200);
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(limitSwitchPin, INPUT_PULLUP);
  
  SerialBT.begin("ESP32"); // Set the Bluetooth name
  Serial.println("Bluetooth Enabled");

}

void loop() {
  // Read the HC-SR04 distance
  long duration, distance;
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1; // Calculate distance in centimeters
  Serial.print("Distance=");
  Serial.println(distance);

  
  // Read the limit switch state
  int limitSwitchState = digitalRead(limitSwitchPin);
    //Serial.print("limitSwitchState=");
    //Serial.println(limitSwitchState);

    if(limitSwitchState==1)
    {
      Serial.print("lid close ");
    }
    else
    {
       Serial.print("lid open ");
    }

  // Send data via Bluetooth
  SerialBT.print("Distance: ");
  SerialBT.print(distance);
  SerialBT.print(" cm, Limit Switch: ");
  SerialBT.println(limitSwitchState);
  
  delay(1000); // Adjust the delay as needed
}
