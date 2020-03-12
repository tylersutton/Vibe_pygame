import pygame

class HealthBar:
    def __init__(self, hp, max_hp, bg_color, fg_color, x, y, width, height):
        self.hp = hp
        self.max_hp = max_hp
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = self.get_sprite()
    
    def update(self, hp, max_hp):
        self.hp = hp
        self.max_hp = max_hp
        self.sprite = self.get_sprite()

    def get_sprite(self):
        fill_percent = min(self.hp / self.max_hp, 1)
        sprite = pygame.Surface((self.width, self.height))
        sprite.fill((self.bg_color))
        if fill_percent > 0:
            fg_sprite = pygame.Surface((int(self.width*fill_percent), self.height))
            fg_sprite.fill((self.fg_color))
            sprite.blit(fg_sprite, (0,0))
        return sprite.convert_alpha()

