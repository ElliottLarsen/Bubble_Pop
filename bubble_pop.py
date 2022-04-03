# Author: Elliott Larsen
# Date:
# Description: 

import os
import pygame

#------------------------------------------
# Set the default environment for the game.
#------------------------------------------
pygame.init()
# Set the screen size.
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bubble Pop")
clock = pygame.time.Clock()

#--------------------
# Set the background.
#--------------------

# Get current directory path.
path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(path, "bg.png"))

condition = True
while condition:
    # Fixed FPS of 55.
    clock.tick(55)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition = False

    # Put the background image at the top left corner.
    screen.blit(background, (0, 0))
    pygame.display.update()

pygame.quit()
