import math

import pygame

def load_sprite(file_name):
    sprite = pygame.image.load(f"{file_name}")
    sprite = sprite.convert_alpha()
    sprite = pygame.transform.smoothscale(sprite, (20, 20))
    return sprite

def get_shadow(darken_percentage, shadow_x, shadow_y):
    if (0 <= darken_percentage <= 100):
        alpha_val = int(255 * darken_percentage / 100)
        blueness = int(40 - (40 * darken_percentage / 100))
        image = pygame.Surface((shadow_x, shadow_y)).convert_alpha()
        image.fill((0, 0, blueness, alpha_val))
    return image

def render_all(game_map, fov_map, fov_radius, player, entities, screen):
    screen.fill((0,0,0))
    screen_width, screen_height = screen.get_width(), screen.get_height()
    new_width = screen_width // game_map.width
    new_height = screen_height // game_map.height
    shadow_darkness = 70

    # print packground tiles (GameMap) first
    for x in range(0, game_map.width):
        for y in range(0, game_map.height):
            visible = fov_map[x][y]
            explored = game_map.bg_tiles[x][y].explored
            if visible:
                game_map.bg_tiles[x][y].explored = True
            if visible or explored:
                screen.blit(game_map.bg_tiles[x][y].sprite, (x*new_width, y*new_height))
    
    # then print map tiles
    for x in range(0, game_map.width):
        for y in range(0, game_map.height):
            visible = fov_map[x][y]
            explored = game_map.tiles[x][y].explored
            if visible:
                game_map.tiles[x][y].explored = True
            if visible or explored:
                screen.blit(game_map.tiles[x][y].sprite, (x*new_width, y*new_height))

    # print entities to screen
    for entity in entities:
        # entity.sprite.set_colorkey((0,0,0))
        entity.sprite = pygame.transform.smoothscale(entity.sprite, (new_width, new_height))
        screen.blit(entity.sprite, (entity.x * new_width, entity.y * new_height))

    # print shadows
    for x in range(0, game_map.width):
        for y in range(0, game_map.height):
            visible = fov_map[x][y]
            explored = game_map.tiles[x][y].explored
            if visible:
                dist = math.sqrt((x - player.x)**2 + (y-player.y)**2)
                darken_percentage = dist / fov_radius * shadow_darkness
            elif explored:
                darken_percentage = shadow_darkness
            if visible or explored:
                shadow = get_shadow(darken_percentage, new_width, new_height)
                screen.blit(shadow, (x*new_width, y*new_height))



    # print player to screen
    # player.sprite.set_colorkey((0,0,0))
    #player.sprite = pygame.transform.smoothscale(player.sprite, (20, 20))
    screen.blit(player.sprite, (player.x * new_width, player.y * new_height))

    # show the new display on screen
    pygame.display.flip()
