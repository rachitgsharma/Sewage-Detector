import random
import tkinter as tk
from tkinter import ttk

# Function to simulate sensor data (replace with actual data acquisition)
def get_sensor_data():
    return {
        "Sensor Data": random.randint(0, 100),
        "Pot Hole Status": random.choice(["ACTIVE", "INACTIVE"]),
        "Overflow": random.choice([True, False])
    }

# Function to update the sensor data display
def update_sensor_data(sensor_label, pothole_status_label, overflow_status_label):
    sensor_data = get_sensor_data()

    # Update sensor data label with increased font size, left alignment, bold font, and background color
    sensor_label.config(
        text=f"Sensor Data: {sensor_data['Sensor Data']}",
        font=("Atma", 40, "bold"),  # Use the "Atma" font with a large font size and bold style
        anchor="w",  # Left align the text
        background="#FBC236"  # Set background color to #FBC236
    )

    # Pot Hole Status with color coding, increased font size, left alignment, bold font, and background color
    pothole_status = sensor_data['Pot Hole Status']
    pothole_status_label.config(
        text=f"Pot Hole Status: {pothole_status}",
        font=("Atma", 30, "bold"),  # Use the "Atma" font with a large font size and bold style
        fg="green" if pothole_status == "ACTIVE" else "red",
        anchor="w",  # Left align the text
        background="#FBC236"  # Set background color to #FBC236
    )

    # Overflow Status with color coding, increased font size, left alignment, bold font, and background color
    overflow_status = "True" if sensor_data['Overflow'] else "False"
    overflow_status_label.config(
        text=f"Overflow: {overflow_status}",
        font=("Atma", 30, "bold"),  # Use the "Atma" font with a large font size and bold style
        fg="green" if sensor_data['Overflow'] else "red",
        anchor="w",  # Left align the text
        background="#FBC236"  # Set background color to #FBC236
    )
