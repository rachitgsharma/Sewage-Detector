# Sewage Detector
## Overview of the Project:
This project is being developed to reduce sewage water overflow.

## Installation
1. Clone the repository:
2. Install Depedencies
 ```text 
 pip install pygame
 pip install matplotlib
 pip install paho-mqtt

```
## Usage
1. Run the main script:
 ```text 
 python main.py
 ``` 
2. The GUI will display real-time sensor data received via MQTT.

## Code Structure
- `main.py`: Main script to run the GUI.
- `sensor_data_display.py`: Module containing functions to display sensor data.
- `constants.py`: Configuration constants for MQTT, display settings, etc.
- `mqtt_client.py`: MQTT client module to handle communication with the broker.

## Configuration
- Update `constants.py` with your MQTT broker details.
- Make sure the ESP32 publishes sensor data to the correct MQTT topics.

## Contributing
Please feel free to contribute to this project by submitting bug reports, feature requests, or pull requests.



