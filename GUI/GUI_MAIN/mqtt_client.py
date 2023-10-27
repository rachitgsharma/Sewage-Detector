import paho.mqtt.client as mqtt
import json

# MQTT broker settings
MQTT_BROKER = "your_broker_address"
MQTT_PORT = 1883
MQTT_TOPIC_DISTANCE = "sensor/distance"
MQTT_TOPIC_LIMIT_SWITCH = "sensor/limit_switch"
MQTT_TOPIC_SENSOR_DATA = "sensor/data"  # Update this topic based on your requirements

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the MQTT topics
    client.subscribe([(MQTT_TOPIC_DISTANCE, 0), (MQTT_TOPIC_LIMIT_SWITCH, 0)])

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    
    global sensor_data
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode('utf-8')}")
    if msg.topic == MQTT_TOPIC_DISTANCE:
        distance_data = float(msg.payload)
        sensor_data["Water Sensor"] = distance_data
    elif msg.topic == MQTT_TOPIC_LIMIT_SWITCH:
        limit_switch_data = msg.payload.decode("utf-8")
        sensor_data["Lid Status"] = limit_switch_data

# Initialize the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Sensor data dictionary
sensor_data = {
    "Node Status": "Active",  # Assuming it's always "Active"
    "Lid Status": "Active",   # Assuming it's always "Active"
    "Date and Time": "",     # To be updated based on your requirements
    "Quick Alerts": "No alerts at the moment",
    "Water Sensor": 0.0,     # Initial value, to be updated by MQTT
}

# Start the MQTT client loop
client.loop_start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Disconnected")
    client.disconnect()
