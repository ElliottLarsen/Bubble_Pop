# Author: Elliott Larsen
# Date: 6/14/2022
# Description: Bubble class.

import pygame
import math
from assets import *

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

    def drop_downward(self, height):
        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery + height))
