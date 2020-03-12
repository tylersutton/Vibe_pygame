import pygame
from pygame_gui.core import UIWindow
from pygame_gui.elements import UITextBox

import textwrap

class Message:
    def __init__(self, text, color=""):
        self.html_text = self.format_text(text, color)
    
    def format_text(self, text, color=""):
        formatted_text = ""
        if color == "":
            formatted_text = text
        else:
            formatted_text = "<body bgcolor = \'#" + color + "\'>" + text + "</body>"
        return formatted_text

class MessageLog:
    def __init__(self, x, y, width, height, manager):
        self.text = "Ayy!<br>"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.manager = manager
        self.text_box = UITextBox(self.text, 
            pygame.Rect((self.x, self.y), (self.width, self.height)), self.manager)

    def add_message(self, message_text, message_color=""):
        message = Message(text=message_text, color=message_color)
        self.text += message.html_text + "<br>"
        if self.text_box:
            self.text_box.kill()
        
        self.text_box = UITextBox(self.text, 
            pygame.Rect((self.x, self.y), (self.width, self.height)), self.manager)
        
        if self.text_box.scroll_bar:
            scroll_bar = self.text_box.scroll_bar
            scroll_bar.scroll_wheel_down = False
            scroll_bar.scroll_position += (250.0 * 1)
            scroll_bar.scroll_position = min(scroll_bar.scroll_position,
                                             scroll_bar.bottom_limit - scroll_bar.sliding_button.rect.height)
            x_pos = scroll_bar.rect.x + scroll_bar.shadow_width + scroll_bar.border_width
            y_pos = scroll_bar.scroll_position + scroll_bar.rect.y + scroll_bar.shadow_width + \
                    scroll_bar.border_width + scroll_bar.button_height
            scroll_bar.sliding_button.set_position(pygame.math.Vector2(x_pos, y_pos))

            scroll_bar.start_percentage = scroll_bar.scroll_position / scroll_bar.scrollable_height
            if not scroll_bar.has_moved_recently:
                scroll_bar.has_moved_recently = True
            