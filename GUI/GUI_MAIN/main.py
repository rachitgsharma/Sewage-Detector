import pygame
import sensor_data_display
from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raspberry Pi Sensor Data")

def main():
    sensor_data_display.welcome_screen()
    running = True
    update_interval = 1000
    last_update_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        if current_time - last_update_time >= update_interval:
            sensor_data_display.sensor_data_screen()
            last_update_time = current_time

    pygame.quit()

if __name__ == "__main__":
    main()
