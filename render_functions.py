import math

import pygame

def load_sprite(file_name):
    sprite = pygame.image.load(f"{file_name}")
    return sprite.convert_alpha()

def darken_sprite(image, darken_percentage):
    if (0 <= darken_percentage <= 100):
        alpha_val = int(255 * darken_percentage / 100)
        blueness = int(40 - (40 * darken_percentage / 100))
        temp_image = image.copy()
        temp_image.fill((0,0,blueness,alpha_val))
        image.blit(temp_image, (0,0))
    return image

def render_all(game_map, fov_map, fov_radius, player, entities, screen):
    screen.fill((255, 255, 255))
    screen_width, screen_height = screen.get_width(), screen.get_height()
    new_width = screen_width // game_map.width
    new_height = screen_height // game_map.height

    # print packground tiles (GameMap) first
    for x in range(0, game_map.width):
        for y in range(0, game_map.height):
            visible = fov_map[x][y]
            
            image = game_map.bg_tiles[x][y].sprite
            image = pygame.transform.smoothscale(image, (new_width, new_height))
            if not visible:
                if game_map.bg_tiles[x][y].explored:
                    image = darken_sprite(image, 70)
                else:
                    image = darken_sprite(image, 100)
            else:
                dist = math.sqrt((x - player.x)**2 + (y-player.y)**2)
                darken_percentage = dist / fov_radius * 70
                image = darken_sprite(image, darken_percentage)
                game_map.bg_tiles[x][y].explored = True
            # image.set_colorkey((0,0,0))
            
            screen.blit(image, (x*new_width, y*new_height))
    
    # then print map tiles
    for x in range(0, game_map.width):
        for y in range(0, game_map.height):
            visible = fov_map[x][y]
            explored = game_map.tiles[x][y].explored
            image = game_map.tiles[x][y].sprite
            image = pygame.transform.smoothscale(image, (new_width, new_height))
            if not visible:
                if explored:
                    image = darken_sprite(image, 70)
                else:
                    image = darken_sprite(image, 100)
            else:
                dist = math.sqrt((x - player.x)**2 + (y-player.y)**2)
                darken_percentage = dist / fov_radius * 70
                image = darken_sprite(image, darken_percentage)
                game_map.tiles[x][y].explored = True
            
            screen.blit(image, (x*new_width, y*new_height))

    # print entities to screen
    for entity in entities:
        # entity.sprite.set_colorkey((0,0,0))
        entity.sprite = pygame.transform.smoothscale(entity.sprite, (new_width, new_height))
        screen.blit(entity.sprite, (entity.x * new_width, entity.y * new_height))

    # print player to screen
    # player.sprite.set_colorkey((0,0,0))
    player.sprite = pygame.transform.smoothscale(player.sprite, (new_width, new_height))
    screen.blit(player.sprite, (player.x * new_width, player.y * new_height))

    # show the new display on screen
    pygame.display.flip()
