import paho.mqtt.client as mqtt
import json
import time
import sensor_data_display
# MQTT broker configuration
MQTT_BROKER_HOST = "your_mqtt_broker_host"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_DISTANCE = "water_sensor_data"
MQTT_TOPIC_LIMIT_SWITCH = "lid_status"

# Initialize the MQTT client
client = mqtt.Client("RaspberryPiSensorClient")

# Store values for calculating average water level
average_water_level_values = []

# Callback function when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code " + str(rc))
    # Subscribe to relevant topics
    client.subscribe(MQTT_TOPIC_DISTANCE)
    client.subscribe(MQTT_TOPIC_LIMIT_SWITCH)

# Callback function to handle incoming MQTT messages
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    sensor_data = json.loads(payload)
    average_water_level_values.append(sensor_data["Water Sensor"])
    average_water_level = sum(average_water_level_values) / len(average_water_level_values)
    sensor_data["Average Water Level"] = round(average_water_level, 2)
    
    # Pass the sensor data to the display function
    sensor_data_display.sensor_data_screen(sensor_data)

# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

# Start the MQTT client loop
client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Disconnected from MQTT broker")
    client.disconnect()
