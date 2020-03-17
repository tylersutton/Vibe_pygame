import math
import pygame

from game_states import GameStates
from ui.elements.inventory_menu import InventoryMenu
from profiler import profile

from enum import Enum

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def load_sprite(file_name, sprite_size):
    sprite = pygame.image.load(f"{file_name}")
    sprite = sprite.convert_alpha()
    sprite = pygame.transform.smoothscale(sprite, sprite_size)
    return sprite

def get_shadow(darken_percentage, shadow_x, shadow_y):
    if (0 <= darken_percentage <= 100):
        alpha_val = int(255 * darken_percentage / 100)
        blueness = int(40 - (40 * darken_percentage / 100))
        image = pygame.Surface((shadow_x, shadow_y)).convert_alpha()
        image.fill((0, 0, blueness, alpha_val))
    return image

def get_map_coords(mouse_x, mouse_y, tile_width, tile_height, camera, map_surf):
    tile_x = (mouse_x - map_surf.x)//tile_width + camera.x
    tile_y = (mouse_y - map_surf.y)//tile_height + camera.y
    return tile_x, tile_y

def get_names_under_mouse(tile_x, tile_y, entities, fov_map):
    names = [entity.name for entity in entities
             if entity.x == tile_x and entity.y == tile_y and fov_map[entity.x][entity.y]]
    names = ', '.join(names)

    return names.capitalize()

# @profile
def render_all(game_map, map_surf, camera, fov_map, fov_radius, player, entities, screen, manager, screen_health_bar, entity_info, game_state):
    # clear surfaces from last frame
    screen.fill((0,0,0))
    map_surf.clear_sprite()

    new_width = map_surf.width // camera.width
    new_height = map_surf.height // camera.height
    shadow_darkness = 70
    # print packground tiles (GameMap) first
    for x in range(camera.x, camera.x + camera.width):
        for y in range(camera.y, camera.y + camera.height):
            if (0 <= x < game_map.width and 0 <= y < game_map.height):
                visible = fov_map[x][y]
                explored = game_map.bg_tiles[x][y].explored
                if visible:
                    game_map.bg_tiles[x][y].explored = True
                if visible or explored:
                    map_surf.add_sprite(game_map.bg_tiles[x][y].sprite, (x - camera.x)*new_width, (y-camera.y)*new_height)
                    # map_surf.blit(game_map.bg_tiles[x][y].sprite, (x*new_width, y*new_height))
    
    # then print map tiles
    for x in range(camera.x, camera.x + camera.width):
        for y in range(camera.y, camera.y + camera.height):
            if (0 <= x < game_map.width and 0 <= y < game_map.height):
                visible = fov_map[x][y]
                explored = game_map.tiles[x][y].explored
                if visible:
                    game_map.tiles[x][y].explored = True
                if visible or explored:
                    map_surf.add_sprite(game_map.tiles[x][y].sprite, (x - camera.x)*new_width, (y-camera.y)*new_height)
                    # map_surf.blit(game_map.tiles[x][y].sprite, (x*new_width, y*new_height))

    # print entities to map
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    
    for entity in entities_in_render_order:
        visible = fov_map[entity.x][entity.y]
        if visible:
            map_surf.add_sprite(entity.sprite, (entity.x-camera.x)*new_width, (entity.y-camera.y)*new_height)
            # map_surf.blit(entity.sprite, (entity.x * new_width, entity.y * new_height))

    # print shadows to map
    for x in range(camera.x, camera.x + camera.width):
        for y in range(camera.y, camera.y + camera.height):
            if (0 <= x < game_map.width and 0 <= y < game_map.height):
                visible = fov_map[x][y]
                explored = game_map.tiles[x][y].explored
                if visible:
                    dist = math.sqrt((x - player.x)**2 + (y-player.y)**2)
                    darken_percentage = dist / fov_radius * shadow_darkness
                elif explored:
                    darken_percentage = shadow_darkness
                if visible or explored:
                    shadow = get_shadow(darken_percentage, new_width, new_height)
                    map_surf.add_sprite(shadow, (x-camera.x)*new_width, (y-camera.y)*new_height)
                    # map_surf.blit(shadow, (x*new_width, y*new_height))

    #blit map onto screen
    screen.blit(map_surf.sprite, (map_surf.x, map_surf.y))

    # update, draw health bar if necessary
    if screen_health_bar.hp != player.fighter.hp or screen_health_bar.max_hp != player.fighter.max_hp:
        screen_health_bar.update(player.fighter.hp, player.fighter.max_hp)
    screen.blit(screen_health_bar.sprite, (screen_health_bar.rect.x, screen_health_bar.rect.y))
    
    # update, draw entity info
    mouse_x, mouse_y = pygame.mouse.get_pos()
    tile_x, tile_y = get_map_coords(mouse_x, mouse_y, new_width, new_height, camera, map_surf)
    entity_info.update_text(get_names_under_mouse(tile_x, tile_y, entities, fov_map))

    screen.blit(entity_info.get_sprite(), (entity_info.rect.x, entity_info.rect.y))

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY) and not manager.inventory_menu:
        inv_rect = pygame.Rect((map_surf.x, map_surf.y), (map_surf.width, map_surf.height))
        text = "Inventory    (click or press correspoding key to use)"
        if game_state == GameStates.DROP_INVENTORY:
            text = "Inventory    (click or press correspoding key to drop)"
        
        inv_menu = InventoryMenu(inv_rect, text, player.inventory, manager.gui)
        manager.init_inventory_menu(inv_menu)
        
    elif game_state not in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY) and manager.inventory_menu:
        manager.delete_inventory_menu()

    manager.gui.draw_ui(screen)

    # show the new display on screen
    pygame.display.flip()
