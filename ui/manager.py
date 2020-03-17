import pygame_gui

class UIManager:
    def __init__(self, width, height, theme):
        self.width = width
        self.height = height
        self.gui = pygame_gui.UIManager((self.width, self.height), theme)
        self.message_log = None
        self.inventory_menu = None
        self.load_fonts()

    def update(self, time_delta):
        self.gui.update(time_delta)

    def load_fonts(self):
        self.gui.add_font_paths("data", "assets/fonts/data-latin.ttf")

    def init_message_log(self, message_log):
        self.message_log = message_log

    def init_inventory_menu(self, inventory_menu):
        self.inventory_menu = inventory_menu

    def add_to_message_log(self, message):
        self.message_log.add_message(message)

    def delete_inventory_menu(self):
        self.inventory_menu.kill()
        self.inventory_menu = None        