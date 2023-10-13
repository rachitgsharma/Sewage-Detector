import pygame
import time
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (24, 24, 24)
INFO_BOX_COLOR = (31, 31, 31)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 32
SMALL_FONT_SIZE = 20
FONT_NAME = 'Arial'
GRAPH_BOX_COLOR = (90, 90, 90)
GRAPH_BOX_WIDTH = 110
GRAPH_BOX_HEIGHT = 240
GRAPH_WIDTH = 240
GRAPH_HEIGHT = 255
GRAPH_BOX_RADIUS = 15

# Thinness of the graph bars
GRAPH_BAR_WIDTH = 0.6

# Create an empty icon surface to remove the window icon
icon_surface = pygame.Surface((1, 1))

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raspberry Pi Sensor Data")
pygame.display.set_icon(icon_surface)

# Create fonts for text
font = pygame.font.Font(None, FONT_SIZE)
small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

# Function to display the welcome screen
def welcome_screen():
    screen.fill(BACKGROUND_COLOR)
    text = font.render("Welcome to Sensor Data Collection", True, FONT_COLOR)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(0.5)

# Function to generate mock sensor data
def generate_sensor_data():
    current_time = time.localtime()
    node_status = "Active" if random.randint(0, 1) == 1 else "Down"
    water_sensor_data = round(random.randint(0, 100), 2)
    lid_status = "Active" if random.randint(0, 1) == 1 else "Down"
    current_datetime = time.strftime("%d %b, %H:%M:%S", current_time)
    average_water_level = round(random.randint(0, 100), 2)
    quick_alerts = "No alerts at the moment"

    return {
        "Node Status": node_status,
        "Water Sensor": water_sensor_data,
        "Lid Status": lid_status,
        "Date and Time": current_datetime,
        "Average Water Level": average_water_level,
        "Quick Alerts": quick_alerts,
    }

# Function to display sensor data
def sensor_data_screen():
    sensor_data = generate_sensor_data()
    
    screen.fill(BACKGROUND_COLOR)

    # Draw a rounded rectangle for the info box
    info_box_rect = pygame.Rect(30, 30, 740, 540)
    pygame.draw.rect(screen, INFO_BOX_COLOR, info_box_rect, border_radius=15)

    # Render sensor data
    render_sensor_data("Node Status:", sensor_data["Node Status"], 50)
    render_sensor_data("Lid Status:", sensor_data["Lid Status"], 150)
    water_sensor_data=sensor_data["Water Sensor"]
    render_sensor_data("Water Level:", f"{water_sensor_data}%", 250)
    render_sensor_data("Date and Time:", sensor_data["Date and Time"], 350)
    avg_water_lvl=sensor_data["Average Water Level"]
    render_sensor_data("Average Water Level:", f"{avg_water_lvl}%", 450)
    render_sensor_data("Quick Alerts:", sensor_data["Quick Alerts"], 540)

    # Replace the custom graph with a Matplotlib graph
    draw_matplotlib_graph(600, 100, GRAPH_WIDTH, GRAPH_HEIGHT, sensor_data["Water Sensor"])

    # Draw a box around the graph and scale
    draw_graph_and_scale_box(600, 100, GRAPH_BOX_WIDTH, GRAPH_BOX_HEIGHT)

    pygame.display.update()

# Function to render sensor data
def render_sensor_data(label, value, y):
    label_text = font.render(label, True, FONT_COLOR)
    value_text = font.render(str(value), True, FONT_COLOR)

    # Customize the font color based on the value
    if value == "Active":
        value_text = font.render(value, True, (0, 255, 0))  # Green for "Active"
    elif value == "Down":
        value_text = font.render(value, True, (255, 0, 0))  # Red for "Down"

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

    # Adjust the x-axis limits to add a gap between the bar and scale
    ax.bar(bar_positions, water_level, width=bar_width, color='white', edgecolor='white')
    ax.set_xlim(0.0, 0.3)  # Adjusted limits to create a gap

    ax.set_ylim(0, 100)
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

    # Format the scale values as percentages and adjust the position
    ax.set_yticklabels(['{:d}%'.format(int(x)) for x in ax.get_yticks()])

    # Add the x-axis label "Water Level (%)"
    ax.set_xlabel('\nWater\nLevel(%)', color='white', horizontalalignment='left',x=0)

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

# Initial welcome screen
welcome_screen()

# Main loop
running = True
update_interval = 1000  # Update every 1 second (in milliseconds)
last_update_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()
    
    if current_time - last_update_time >= update_interval:
        # Switch to the sensor data screen
        sensor_data_screen()
        last_update_time = current_time

# Quit Pygame
pygame.quit()
