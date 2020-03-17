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
                                                 text=f"{inventory.items[item_slot].name}" + "[" + f"{inventory.items[item_slot].item.count}" + "] (" + chr(ord('a')+item_slot) + ")", manager=manager,
                                                 container=self.get_container(),
                                                 object_id=f"#item_button{item_slot}"))
    
    def kill(self):
        self.text_box.kill()
        for i in range(0, len(self.buttons)):
            self.buttons[i].kill()