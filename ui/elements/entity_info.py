import pygame

class EntityInfo:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font('assets/fonts/data-latin.ttf', self.height)
        self.text = "the fuck"
        self.sprite = self.get_sprite()

    def get_sprite(self):
        sprite = pygame.Surface((self.width, self.height))
        text_sprite = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_sprite.get_rect()
        sprite.blit(text_sprite, text_rect)
        return sprite

    def update_text(self, text):
        self.text = text