import pygame_gui

class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gui = pygame_gui.UIManager((self.width, self.height))
        self.message_log = None
    
    def update(self, time_delta):
        self.gui.update(time_delta)

    def init_message_log(self, message_log):
        self.message_log = message_log

    def add_to_message_log(self, message):
        self.message_log.add_message(message)
        