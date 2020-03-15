import pygame

class HealthBar:
    def __init__(self, name, hp, max_hp, bg_color, fg_color, x, y, width, height):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font('assets/fonts/data-latin.ttf', self.height//2)
        self.sprite = self.get_sprite()
        
    def update(self, hp, max_hp):
        self.hp = hp
        self.max_hp = max_hp
        self.sprite = self.get_sprite()

    def get_sprite(self):
        fill_percent = min(self.hp / self.max_hp, 1)
        sprite = pygame.Surface((self.width, self.height))
        health_text = self.name + ' hp: ' + str(self.hp) + '/' + str(self.max_hp)
        text = self.font.render(health_text, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.width//2, self.height//4)

        sprite.blit(text, text_rect)
        bg_sprite = pygame.Surface((self.width, self.height//2))
        bg_sprite.fill((self.bg_color))
        sprite.blit(bg_sprite, (0, self.height//2))
        if fill_percent > 0:
            fg_sprite = pygame.Surface((int(self.width*fill_percent), self.height//2))
            fg_sprite.fill((self.fg_color))
            sprite.blit(fg_sprite, (0, self.height//2))
        return sprite.convert_alpha()

