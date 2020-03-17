import pygame

class EntityInfo:
    def __init__(self, rect):
        self.rect = rect
        self.font = pygame.font.Font('assets/fonts/data-latin.ttf', self.rect.height)
        self.text = ""
        self.sprite = self.get_sprite()

    def get_sprite(self):
        sprite = pygame.Surface((self.rect.width, self.rect.height))
        text_sprite = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_sprite.get_rect()
        sprite.blit(text_sprite, text_rect)
        return sprite

    def update_text(self, text):
        self.text = text