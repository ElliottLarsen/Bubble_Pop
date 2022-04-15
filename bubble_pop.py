# Author: Elliott Larsen
# Date:
# Description: 

import os
import pygame
import random
import math

class Bubble(pygame.sprite.Sprite):
    """
    Represents a bubble class.
    """
    def __init__(self, image, color, position = (0, 0)):
        """
        Creates an instance of a bubble.
        """
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center = position)
        self.radius = 15

    def set_rect(self, position):
        """
        This method receives position as parameter and sets the class's rect to it.
        """
        self.rect = self.image.get_rect(center = position)

    def draw(self, screen):
        """
        This method receives screen as parameter and draws the bubble object on the screen.
        """
        screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        """
        This method receives an angle as parameter and sets the bubble's angle to it (radian).
        """
        self.angle = angle
        self.rad_angle = math.radians(self.angle)

    def move(self):
        """
        This method calculates and sets x and y coordinates of the bubble.
        """
        x_coord = self.radius * math.cos(self.rad_angle)
        y_coord = self.radius * math.sin(self.rad_angle) * -1

        self.rect.x += x_coord
        self.rect.y += y_coord

        # When the bubble hits the wall.
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)

class Arrow(pygame.sprite.Sprite):
    """
    Represents a shooting arrow class.
    """
    def __init__(self, image, position, angle):
        """
        Creates an instance of a shooting arrow.
        """
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center = position)
        self.angle = angle
        self.original = image
        self.position = position

    def draw(self, screen):
        """
        This method receives screen as parameter and draws the arrow object on the screen.
        """
        screen.blit(self.image, self.rect)

    def rotate(self, angle):
        """
        This method receives angle as parameter and rotates the arrow.
        """
        self.angle += angle
        
        if self.angle > 150:
            self.angle = 150
        elif self.angle < 30:
            self.angle = 30

        self.image = pygame.transform.rotozoom(self.original, self.angle, 1)
        self.rect = self.image.get_rect(center = self.position)
        
def set_map():
    """
    This function populates the initial map with the bubbles.
    """
    global map
    # Letters indicate colors.  N indicates the location where no bubble is permitted to go and . indicates an empty space.
    map = [
        list("BBGGRRYY"), 
        list("BGGRRYYN"), 
        list("RRYYBBGG"), 
        list("RRYYBBGN"), 
        list("........"), 
        list(".......N"), 
        list("........"), 
        list(".......N"), 
        list("........"), 
        list(".......N"), 
        list("........")
    ]

    # Populate the map with bubbles.
    for row_index, row in enumerate(map):
        # Column is equal to a letter, which represents the color or status of the cell.
        for column_index, column in enumerate(row):
            if column == "N" or column == ".":
                continue
            location = get_bubble_location(row_index, column_index)
            image = get_bubble_image(column)
            bubble = Bubble(image, column, location)
            bubble_group.add(bubble)

def get_bubble_location(row_index, column_index):
    """
    This function receives the row and column indices and returns the bubble's location.
    """
    x_coord = column_index * cell_size + (bubble_width // 2)
    y_coord = row_index * cell_size + (bubble_height // 2)
    # If the bubble is located in the even-numbered rows (or odd=numbered indices), it needs to be offset to the right by half of the bubble width.
    if row_index % 2 == 1:
        x_coord += bubble_width // 2
    
    return (x_coord, y_coord)

def get_bubble_image(color):
    """ 
    This function receives a color (represented by a letter) and returns the corresponding image for the bubble.
    """
    if color == "B":
        return bubble_images[1]
    
    elif color == "G":
        return bubble_images[2]

    elif color == "P":
        return bubble_images[3]
    
    elif color == "R":
        return bubble_images[4]

    elif color == "Y":
        return bubble_images[5]
    else:
        return bubble_images[0]

def setup_bubbles():
    """
    Creates and sets up a bubble.
    """
    global current_bubble, next_bubble
    
    if next_bubble:
        current_bubble = next_bubble
    else:
        current_bubble = create_bubble()
    
    current_bubble.set_rect((screen_width // 2, 624))
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width // 3, 660))

def create_bubble():
    """
    This function creates a bubble of randomly picked color.
    """
    color = get_random_color()
    image = get_bubble_image(color)
    
    return Bubble(image, color)

def get_random_color():
    """
    Picks a randome color for the bubble.
    """
    colors = []
    for row in map:
        for column in row:
            if column not in colors and column not in [".", "N"]:
                colors.append(column)
    
    return random.choice(colors)

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

#-----------------
# Set the bubbles.
#-----------------
# List of bubble images.
bubble_images = [
    pygame.image.load(os.path.join(path, "black.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "yellow.png")).convert_alpha()
]

#------------------------
# Set the shooting arrow.
#------------------------
bubble_arrow = pygame.image.load(os.path.join(path, "arrow.png"))
arrow = Arrow(bubble_arrow, (screen_width // 2, 624), 90)

# Variables/assets/info for the game.
cell_size = 56
bubble_width = 56
bubble_height = 62
angle_left = 0
angle_right = 0
angle_speed = 1.5 # Move the arrow by 1.5 degrees.

current_bubble = None # Current bubble placed on the arrow.
next_bubble = None # Next bubble to be placed on the arrow.
fire = False # Whether the bubble that has been fired is in motion..

map = []
bubble_group = pygame.sprite.Group()

set_map()
condition = True
while condition:
    # Fixed FPS of 55.
    clock.tick(55)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition = False

        # Move the arrow by 1.5 degrees if the key is pressed.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle_left += angle_speed
            elif event.key == pygame.K_RIGHT:
                angle_right -= angle_speed
            elif event.key == pygame.K_SPACE:
                # So that the bubble can be fired only if the current bubble is not None and there is no bubble in motion.
                if current_bubble and not fire:
                    fire = True
                    current_bubble.set_angle(arrow.angle)


        # Stop moving the arrow when the key is not pressed.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                angle_left = 0

            elif event.key == pygame.K_RIGHT:
                angle_right = 0

    if not current_bubble:
        setup_bubbles()

    # Put the background image at the top left corner.
    screen.blit(background, (0, 0))
    bubble_group.draw(screen)
    arrow.rotate(angle_left + angle_right)
    arrow.draw(screen)
    # Draw a bubble on the arrow.
    if current_bubble:
        if fire:
            current_bubble.move()
        current_bubble.draw(screen)

        # Needs to be updated after working out popping the bubbles.
        if current_bubble.rect.top <= 0:
            current_bubble = None
            fire = False
    
    if next_bubble:
        next_bubble.draw(screen)

    pygame.display.update()

pygame.quit()
