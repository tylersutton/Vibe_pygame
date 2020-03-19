import pygame

class MapSurface:
    def __init__(self, rect, map_sprites):
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height
        self.sprite = pygame.Surface((rect.width, rect.height))
        self.map_sprites = map_sprites
    
    def add_sprite(self, sprite, x, y):
        self.sprite.blit(sprite, (x, y))
    
    def clear_sprite(self):
        self.sprite.fill((0,0,0))