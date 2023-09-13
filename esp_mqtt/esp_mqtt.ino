#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "SSID";
const char* password = "PASSWORD";

const char* mqttServer = "IP OF BROKER"; // Replace with your MQTT broker server address
const int mqttPort = 1883;
const char* mqttUser = "mqttUser"; // Replace with your MQTT username
const char* mqttPassword = "mqttPassword"; // Replace with your MQTT password
const char* mqttClientId = "mqttClientId"; // Replace with a unique client ID

WiFiClient espClient;
PubSubClient client(espClient);

const int triggerPin = 13; // HC-SR04 trigger pin
const int echoPin = 12;    // HC-SR04 echo pin
const int limitSwitchPin = 14; // Limit switch input pin

void setup() 
{
  Serial.begin(115200);
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(limitSwitchPin, INPUT_PULLUP);
  
  setup_wifi();
  client.setServer(mqttServer, mqttPort);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(mqttClientId, mqttUser, mqttPassword)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  
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
  if (limitSwitchState == 1) {
    Serial.print("Lid close ");
  } else {
    Serial.print("Lid open ");
  }

  // Publish data via MQTT with specific topics
char distanceTopic[] = "sensor/distance"; // Change this topic to your preference
char limitSwitchTopic[] = "sensor/limit_switch"; // Change this topic to your preference

char distanceStr[10];
snprintf(distanceStr, sizeof(distanceStr), "%ld", distance);
client.publish(distanceTopic, distanceStr);

char limitSwitchStr[2];
snprintf(limitSwitchStr, sizeof(limitSwitchStr), "%d", limitSwitchState);
client.publish(limitSwitchTopic, limitSwitchStr);

  delay(1000); // Adjust the delay as needed
}