# Author: Elliott Larsen
# Date:
# Description:

import os
import pygame

screen_width = 448
screen_height = 720
cell_size = 56
bubble_width = 56
bubble_height = 62
status_message_color = (255, 255, 255)
angle_left = 0
angle_right = 0
angle_speed = 1.5 # Move the arrow by 1.5 degrees.
map_row_count = 11
map_column_count = 8
shoot_count = 7 # Seven bubbles can be shot before the set lowers.

current_bubble = None # Current bubble placed on the arrow.
next_bubble = None # Next bubble to be placed on the arrow.
fire = False # Whether the bubble that has been fired is in motion..
current_shoot_count = shoot_count
wall_height = 0
game_over = False
#font = pygame.font.SysFont('garamond', 40)
game_status = None

map = []
visited = [] # For remove_bubbles()
bubble_group = pygame.sprite.Group()
