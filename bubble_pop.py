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
    def __init__(self, image, color, position = (0, 0), row_index = -1, column_index = -1):
        """
        Creates an instance of a bubble.
        """
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center = position)
        self.radius = 15
        self.row_index = row_index
        self.column_index = column_index

    def set_rect(self, position):
        """
        This method receives position as parameter and sets the class's rect to it.
        """
        self.rect = self.image.get_rect(center = position)

    def draw(self, screen, to_x = None):
        """
        This method receives screen as parameter and draws the bubble object on the screen.  If to_x is 2 (after the fifth bubble is shot), this functio shakes the screen.  After the sixth bubble is shot, the shake becomes stronger.
        """
        if to_x:
            screen.blit(self.image, (self.rect.x + to_x, self.rect.y))
        else:
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

    def set_map_index(self, row_index, column_index):
        """
        Sets the map index.
        """
        self.row_index = row_index
        self.column_index = column_index

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
            bubble = Bubble(image, column, location, row_index, column_index)
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

def collision():
    """
    This function places the bubble when it collides with pre-existing bubbles.
    """
    global current_bubble, fire, current_shoot_count
    hit_bubble = pygame.sprite.spritecollideany(current_bubble, bubble_group, pygame.sprite.collide_mask)
    # If the bubble collides with other bubbles or it hits the ceiling.
    if hit_bubble or current_bubble.rect.top <= 0:
        row_index, column_index = get_map_index(*current_bubble.rect.center)
        place_bubble(current_bubble, row_index, column_index)
        remove_bubbles(row_index, column_index, current_bubble.color)
        current_bubble = None
        fire = False
        current_shoot_count -= 1

def get_map_index(x, y):
    """
    This function receives the x and y coordinates (unpacked from a tuple) as parameters and returns the row and column indices.
    """
    row_index = y // cell_size
    column_index = x // cell_size
    if row_index % 2 == 1:
        column_index = (x - (cell_size // 2)) // cell_size
        if column_index < 0:
            column_index = 0
        elif column_index > map_column_count - 2:
            column_index = map_column_count - 2

    return row_index, column_index

def place_bubble(bubble, row_index, column_index):
    """
    This function receives the current bubble and row/column indices as parameters and places the bubble on the correct position on the screen.
    """
    map[row_index][column_index] = bubble.color
    position = get_bubble_location(row_index, column_index)
    bubble.set_rect(position)
    bubble.set_map_index(row_index, column_index)
    bubble_group.add(bubble)


def remove_bubbles(row_index, column_index, color):
    """
    This function receives row index, column index, and color as parameters and deletes bubbles if more than three bubbles of the same color come in contact with the new bubble.
    """
    # Reset the visited list.
    visited.clear() 
    visit(row_index, column_index, color)
    # Delete if it collides with at least three bubbles with same color.
    if len(visited) >= 3:
        remove_visited()
        remove_hanging_bubbles()

def visit(row_index, column_index, color = None):
    """
    This function receives row index, column index, and color and parameters and determines which bubbles are visited, much like DFS.
    """
    # Check if the bubble tries move out of the map.
    if row_index < 0 or row_index >= map_row_count or column_index < 0 or column_index >= map_column_count:
        return
    # Check if the current cell's color matches the passed color.
    if color is not None and map[row_index][column_index] != color:
        return
    # Check if an empty space or there is no bubble.
    if map[row_index][column_index] in [".", "N"]:
        return
    # If the cell has already been visited.
    if (row_index, column_index) in visited:
        return
    
    visited.append((row_index, column_index))
    rows = [0, -1, -1, 0, 1, 1]
    columns = [-1, -1, 0, 1, 0, -1]
    if row_index % 2 == 1:
        rows = [0, -1, -1, 0, 1, 1]
        columns = [-1, 0, 1, 1, 1, 0]
    for i in range(len(rows)):
        visit(row_index + rows[i], column_index + columns[i], color)

def remove_visited():
    """
    This function is called from remove_bubbles() and deletes the bubbles from the screen.
    """
    bubbles_to_remove = [i for i in bubble_group if (i.row_index, i.column_index) in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_index][bubble.column_index] = "."
        bubble_group.remove(bubble)

def remove_not_visited():
    """
    This function deletes the bubbles that are not included in visited bubble list.
    """
    bubbles_to_remove = [i for i in bubble_group if (i.row_index, i.column_index) not in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_index][bubble.column_index] = "."
        bubble_group.remove(bubble)

def remove_hanging_bubbles():
    """
    This function removes bubbles that are hanging below deleted bubbles.
    """
    visited.clear()
    for column_index in range(map_column_count):
        if map[0][column_index] != ".":
            visit(0, column_index)
    remove_not_visited()

def draw_bubbles():
    """
    This function draws bubbles on the screen.  After the fifth bubble has been shot, this function adds to_x to the bubble that will be used to shake the screen.
    """
    to_x = None
    if current_shoot_count == 2:
        to_x = random.randint(-1, 1)
    elif current_shoot_count == 1:
        to_x = random.randint(-4, 4)

    for bubble in bubble_group:
        bubble.draw(screen, to_x)
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
map_row_count = 11
map_column_count = 8
shoot_count = 7 # Seven bubbles can be shot before the set lowers.

current_bubble = None # Current bubble placed on the arrow.
next_bubble = None # Next bubble to be placed on the arrow.
fire = False # Whether the bubble that has been fired is in motion..
current_shoot_count = shoot_count

map = []
visited = [] # For remove_bubbles()
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

    if fire:
        collision()

    # Put the background image at the top left corner.
    screen.blit(background, (0, 0))
    #bubble_group.draw(screen)
    draw_bubbles()
    arrow.rotate(angle_left + angle_right)
    arrow.draw(screen)
    # Draw a bubble on the arrow.
    if current_bubble:
        if fire:
            current_bubble.move()
        current_bubble.draw(screen)

        # Needs to be updated after working out popping the bubbles.
        #if current_bubble.rect.top <= 0:
        #    current_bubble = None
        #    fire = False
    
    if next_bubble:
        next_bubble.draw(screen)

    pygame.display.update()

pygame.quit()
