# Author: Elliott Larsen
# Date:
# Description:

import pygame
from assets import *

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