import pygame
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import paho.mqtt.client as mqtt
from constants import *
from datetime import datetime


# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raspberry Pi Sensor Data")

# Create fonts for text
font = pygame.font.Font(None, FONT_SIZE)
small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

# MQTT Configuration
MQTT_BROKER = "sewage.local"  # Replace with your MQTT broker IP
MQTT_PORT = 1883
MQTT_TOPIC_DISTANCE = "sensor/distance"
MQTT_TOPIC_LIMIT_SWITCH = "sensor/limit_switch"

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc)) #connect with mqtt server
    # Subscribe to MQTT topics
    client.subscribe([(MQTT_TOPIC_DISTANCE, 0), (MQTT_TOPIC_LIMIT_SWITCH, 0)])

def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode('utf-8')}") #decode message
    if msg.topic == MQTT_TOPIC_DISTANCE:
        sensor_data["Water Sensor"] = float(msg.payload)
    elif msg.topic == MQTT_TOPIC_LIMIT_SWITCH:
        sensor_data["Lid Status"] = msg.payload.decode("utf-8") #decode message


# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# Function to display the welcome screen
def welcome_screen():
    screen.fill(BACKGROUND_COLOR)
    text = font.render("Welcome to Sensor Data Collection", True, FONT_COLOR)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(0.5)

# Function to display sensor data
def sensor_data_screen(sensor_data):
    screen.fill(BACKGROUND_COLOR)
    # Draw a rounded rectangle for the info box
    info_box_rect = pygame.Rect(30, 30, 740, 540)
    pygame.draw.rect(screen, INFO_BOX_COLOR, info_box_rect, border_radius=15)

    # Render sensor data
    render_sensor_data("Node Status:", sensor_data["Node Status"], 50)
    
    # Update Lid Status display
    lid_status = "Down" if (sensor_data["Lid Status"] == "1") else "Active"
    # lid_status = sensor_data["Lid Status"]
    render_sensor_data("Lid Status:", lid_status, 150)
    
    water_sensor_data = sensor_data["Water Sensor"]
    render_sensor_data("Water Level:", f"{water_sensor_data:.2f} cm", 250)
    
    # Get the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    render_sensor_data("Date and Time:", current_time, 350)
    
    avg_water_lvl = calculate_average_water_level(sensor_data["Water Sensor"])
    render_sensor_data("Average Water Level:", f"{avg_water_lvl:.2f} cm", 450)
    alerts=""
    if ((sensor_data["Lid Status"] == "1") & (int(sensor_data["Water Sensor"]) > 5)):
        alerts = "Check if Lid is Open"
    elif ((sensor_data["Lid Status"] == "0") & (int(sensor_data["Water Sensor"]) > 20)):
        alerts = "No Alerts"
    elif ((sensor_data["Lid Status"] == "1") & (int(sensor_data["Water Sensor"]) <= 5)):
        alerts = "Overflow"
    elif ((sensor_data["Lid Status"] == "0") & (int(sensor_data["Water Sensor"]) <= 20)):
        alerts = "Chances of overflow"
    render_sensor_data("Quick Alerts:",f"{alerts}", 540)

    # Replace the custom graph with a Matplotlib graph
    draw_matplotlib_graph(600, 100, GRAPH_WIDTH, GRAPH_HEIGHT, water_sensor_data)

    # Draw a box around the graph and scale
    draw_graph_and_scale_box(600, 100, GRAPH_BOX_WIDTH, GRAPH_BOX_HEIGHT)

    pygame.display.update()



# Function to render sensor data
def render_sensor_data(label, value, y):
    label_text = font.render(label, True, FONT_COLOR)

    if label == "Lid Status:":
        if value == "Down":
            value_text = font.render("OPEN", True, (255, 0, 0))  # Green for "Down"
        elif value == "Active":
            value_text = font.render("CLOSED", True, (0, 255, 0))  # Red for "ACTIVE"
            
    else:
        value_text = font.render(value, True, FONT_COLOR)

    label_rect = label_text.get_rect()
    value_rect = value_text.get_rect()
    label_x = 50
    value_x = 400
    label_rect.topleft = (label_x, y)
    value_rect.topleft = (value_x, y)
    screen.blit(label_text, label_rect)
    screen.blit(value_text, value_rect)



# Function to draw a Matplotlib graph with a single, thin bar
def draw_matplotlib_graph(x, y, width, height, water_level):
    fig, ax = plt.subplots(figsize=(width / 80, height / 80), dpi=70)

    # Set the number of bars to 1 for a single, thin bar
    num_bars = 1
    bar_width = 0.1
    bar_positions = [0]
    water_level=100-water_level
    # Adjust the x-axis limits to add a gap between the bar and scale
    ax.bar(bar_positions, water_level, width=bar_width, color='white', edgecolor='white')
    ax.set_xlim(0.0, 0.5)  # Adjusted limits to create a gap (0.5 instead of 0.3)

    ax.set_ylim(0, 100)  # Set the y-axis limits to 0-100
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Remove x-axis and y-axis lines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_linewidth(0)
    ax.spines['bottom'].set_linewidth(0)

    # Customize the scale values color to white and add the "%" sign
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='both', colors='white')
    ax.xaxis.label.set_color('white')

    # Set the tick locations and format the scale values as percentages
    ax.set_yticks(range(0, 101, 10))  # Set the tick locations from 0-100 with a step of 10
    ax.set_yticklabels(['{:d}%'.format(int(x)) for x in range(0, 101, 10)])  # Update the range to 0-100% with a step of 10

    # Add the x-axis label "Water Level (%)"
    ax.set_xlabel('Water\nLevel(%)', color='white', horizontalalignment='left', x=0)

    # Adjust the layout to make the numbers fit better
    plt.tight_layout()

    plt.xticks([])

    # Make the graph background transparent
    ax.set_facecolor('none')

    plt.savefig("graph.png", dpi=80, transparent=True)
    plt.close()

    graph = pygame.image.load("graph.png")
    screen.blit(graph, (x, y))




# Function to draw a box around the graph and scale
def draw_graph_and_scale_box(x, y, width, height):
    pygame.draw.rect(screen, GRAPH_BOX_COLOR, pygame.Rect(x, y, width, height), 2, border_radius=GRAPH_BOX_RADIUS)

# Function to calculate the average water level
def calculate_average_water_level(new_value):
    global water_level_values
    water_level_values.append(new_value)
    if len(water_level_values) > WATER_LEVEL_VALUE_COUNT:
        water_level_values.pop(0)
    return sum(water_level_values) / len(water_level_values)

# Sensor data dictionary
sensor_data = {
    "Node Status": "ACTIVE",  # Assuming it's always "Inactive"
    "Lid Status": "UNKNOWN",   # Assuming it's "unknown"
    "Date and Time": "",     # To be updated based on your requirements
    "Quick Alerts": "No alerts at the moment",
    "Water Sensor": 0.0,     # Initial value, to be updated by MQTT
}

# List to store recent water level values for averaging
water_level_values = []

# Initial welcome screen
welcome_screen()

# Main loop
running = True
update_interval = 100  # Update every 1 second (in milliseconds)
last_update_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    if current_time - last_update_time >= update_interval:
        # Fetch data from MQTT and update the GUI
        sensor_data_screen(sensor_data)
        last_update_time = current_time

# Quit Pygame
pygame.quit()
