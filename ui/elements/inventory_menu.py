import pygame
from pygame import UITextBox

class InventoryMenu:
    def __init__(self, x, y, width, height, manager):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.manager = manager
        self.text = ''
        self.text_box = UITextBox(self.text,
            pygame.Rect((self.x, self.y), (self.width, self.height)), self.manager)