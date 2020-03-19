import pygame_gui
from ui.elements.game_messages import MessageLog
from ui.elements.menus import MainMenu, InventoryMenu

class UIManager:
    def __init__(self, width, height, main_menu_rect, message_log_rect, theme):
        self.width = width
        self.height = height
        self.gui = pygame_gui.UIManager((self.width, self.height), theme)
        self.main_menu_rect = main_menu_rect
        self.main_menu = None
        self.inventory_menu = None
        self.message_log_rect = message_log_rect
        self.message_log = None
        self.load_fonts()

    def update(self, time_delta):
        self.gui.update(time_delta)

    def load_fonts(self):
        self.gui.add_font_paths("data", "assets/fonts/data-latin.ttf")

    def init_message_log(self):
        self.message_log = MessageLog(self.message_log_rect, self.gui)

    def add_to_message_log(self, message):
        self.message_log.add_message(message)

    def kill_message_log(self):
        self.message_log.kill()

    def init_inventory_menu(self, inventory_menu):
        self.inventory_menu = inventory_menu

    def kill_inventory_menu(self):
        self.inventory_menu.kill()
        self.inventory_menu = None
    
    def init_main_menu(self):
        self.main_menu = MainMenu(self.main_menu_rect, self.gui)
    
    def kill_main_menu(self):
        self.main_menu.kill()
        self.main_menu = None