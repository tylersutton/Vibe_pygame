import pygame

import pygame_gui
from pygame_gui.core import UIWindow

from ui.elements.game_messages import Message

class InventoryMenu(UIWindow):
    def __init__(self, rect, text, inventory, manager):
        self.rect = rect
        self.inventory = inventory
        self.buttons = []
        self.manager = manager
        self.text = Message(text, size=4).html_text
        self.text_box = pygame_gui.elements.UITextBox(self.text,
            pygame.Rect((self.rect.x, self.rect.y), (self.rect.width, 40)), self.manager, wrap_to_height=False)
        
        super().__init__(rect, manager, ["inventory_menu"])

        start_x = self.rect.x
        start_y = self.rect.y + 50
        width = 200
        height = 30
        gap = 2

        for item_slot in range(0, len(self.inventory.items)):
            x = start_x
            y = start_y + (height * item_slot) + (gap * item_slot)
            self.buttons.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x, y), (width, height)),
                                                 text=f"{inventory.items[item_slot].name}" + "[" + f"{inventory.items[item_slot].item.count}" + "] (" + chr(ord('a')+item_slot) + ")", 
                                                 manager=manager, container=self.get_container(), starting_height=10,
                                                 object_id=f"#item_button{item_slot}"))
    
    def kill(self):
        self.text_box.kill()
        for i in range(0, len(self.buttons)):
            self.buttons[i].kill()


class MainMenu(UIWindow):
    def __init__(self, rect, manager):
        self.rect = rect
        self.manager = manager
        self.text = Message("Vibe", size=4).html_text
        self.text_box = pygame_gui.elements.UITextBox(self.text,
            pygame.Rect((self.rect.x, self.rect.y + 80), (self.rect.width, 80)), self.manager, wrap_to_height=False)
        
        super().__init__(rect, manager, ["main_menu"])
        
        width = 300
        height = 60
        gap = 10
        x = (self.rect.width // 2) - width
        y = (self.rect.height // 2) - (height*2) - gap
        
        self.new_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x, y), (width, height)),
                                                 text="New Game",
                                                 manager=manager, container=self.get_container(), starting_height=10,
                                                 object_id=f"#new_game_button")
        y += height + gap
        self.load_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x, y), (width, height)),
                                                 text="Load Game",
                                                 manager=manager, container=self.get_container(), starting_height=10,
                                                 object_id=f"#load_game_button")
        y += height + gap
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x, y), (width, height)),
                                                 text="Exit",
                                                 manager=manager, container=self.get_container(), starting_height=10,
                                                 object_id=f"#exit_button")

        
    
    def kill(self):
        self.text_box.kill()
        self.new_game_button.kill()
        self.load_game_button.kill()
        self.exit_button.kill()
