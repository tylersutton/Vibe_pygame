import pygame
from pygame_gui.core import UIWindow
from pygame_gui.elements import UITextBox

class Message:
    def __init__(self, text, color=pygame.Color('white'), size=5):
        self.html_text = self.format_text(text, color, size)
    
    """
    convert text to html format 
    """
    def format_text(self, text, color, size):
        color_hex = ""
        if isinstance(color, str):
            color_hex = color
        else:
            for i in range(0, 3):
                color_hex += "%02x" % color[i] # convert color from tuple to hex if necessary
        formatted_text = "<font face=\'data\' color =\'#" + color_hex + "\' size=" + str(size) + ">" + text + "</font>"
        return formatted_text

class MessageLog(UIWindow):
    def __init__(self, rect, manager):
        self.text = Message("Welcome to Vibe!").html_text + "<br>"
        self.rect = rect
        self.text_box = None
        self.manager = manager
        super().__init__(self.rect, manager, ["message_log"])
        self.text_box = UITextBox(self.text, self.rect, self.manager, wrap_to_height=False, layer_starting_height=1)

    def add_message(self, message):
        self.text += message.html_text + "<br>"
        if self.text_box:
            self.text_box.kill()
        
        self.text_box = UITextBox(self.text,
            pygame.Rect((0, 0), (self.rect.width, self.rect.height)), self.manager, wrap_to_height=False, layer_starting_height=1, container=self.get_container())
        self.text_box.parse_html_into_style_data()

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

        