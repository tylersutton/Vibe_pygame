import pygame
from pygame_gui.core import UIWindow
from pygame_gui.elements import UITextBox

import textwrap

class Message:
    def __init__(self, text, color="FFFFFF"):
        self.html_text = self.format_text(text, color)
    
    def format_text(self, text, color="CCCCCC"):
        # <font face=’verdana’ color=’#000000’ size=3.5></font>
        formatted_text = "<font face=\'verdana\' color =\'#" + color + "\' size=8>" + text + "</font>"
        return formatted_text

class MessageLog(UIWindow):
    def __init__(self, x, y, width, height, manager):
        self.text = Message("Welcome to Vibe!").html_text + "<br>"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_box = None
        self.manager = manager
        super().__init__(pygame.Rect((self.x, self.y), (self.width, self.height)), manager, ["message_log"])
        self.text_box = UITextBox(self.text,
            pygame.Rect((self.x, self.y), (self.width, self.height)), self.manager)

    def add_message(self, message_text, message_color="888888"):
        message = Message(text=message_text, color=message_color)
        self.text += message.html_text + "<br>"
        if self.text_box:
            self.text_box.kill()
        
        self.text_box = UITextBox(self.text,
            pygame.Rect((0, 0), (self.width, self.height)), self.manager, wrap_to_height=False, container=self.get_container())
        

        """
        got this from Snayff, not quite sure how it works
        sauce: https://bitbucket.org/Snayff/notquiteparadise/src/develop/scripts/engine/ui/elements/message_log.py
        """

        if self.text_box.scroll_bar:
            scroll_bar = self.text_box.scroll_bar
            scroll_bar.scroll_wheel_down = False
            scroll_bar.scroll_position += (250 * 1)
            scroll_bar.scroll_position = min(scroll_bar.scroll_position,
                                           scroll_bar.bottom_limit - scroll_bar.sliding_button.rect.height)
            x_pos = scroll_bar.rect.x + scroll_bar.shadow_width + scroll_bar.border_width
            y_pos = scroll_bar.scroll_position + scroll_bar.rect.y + scroll_bar.shadow_width + \
                    scroll_bar.border_width + scroll_bar.button_height
            scroll_bar.sliding_button.set_position(pygame.math.Vector2(x_pos, y_pos))

            scroll_bar.start_percentage = scroll_bar.scroll_position / scroll_bar.scrollable_height
            if not scroll_bar.has_moved_recently:
                scroll_bar.has_moved_recently = True

        