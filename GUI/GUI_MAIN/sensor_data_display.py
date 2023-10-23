import pygame
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import json
import paho.mqtt.client as mqtt
from constants import *

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raspberry Pi Sensor Data")

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

# Function to display sensor data
def sensor_data_screen(sensor_data):
    screen.fill(BACKGROUND_COLOR)
    # Draw a rounded rectangle for the info box
    info_box_rect = pygame.Rect(30, 30, 740, 540)
    pygame.draw.rect(screen, INFO_BOX_COLOR, info_box_rect, border_radius=15)

    # Render sensor data
    render_sensor_data("Node Status:", sensor_data["Node Status"], 50)
    render_sensor_data("Lid Status:", sensor_data["Lid Status"], 150)
    water_sensor_data = sensor_data["Water Sensor"]
    render_sensor_data("Water Level:", f"{water_sensor_data}%", 250)
    render_sensor_data("Date and Time:", sensor_data["Date and Time"], 350)
    avg_water_lvl = sensor_data["Average Water Level"]
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
    ax.set_yticklabels(['{:d}%'.format(int(x)) for x in range(int(min(ax.get_yticks())), int(max(ax.get_yticks())) + 1)])

    # Add the x-axis label "Water Level (%)"
    ax.set_xlabel('\nWater\nLevel(%)', color='white', horizontalalignment='left', x=0)

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
