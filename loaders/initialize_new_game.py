import pygame

from components.ai import BasicMonster
from components.fighter import Fighter
from entity import Entity
from map_objects.game_map import GameMap
from render_functions import load_sprite, RenderOrder

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

def get_constants():
    map_width = 50
    map_height = 30
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT

    start_hp = 100
    start_def = 2
    start_power = 5

    max_monsters_per_room = 10

    tile_size = 16
    
    sprites = {
        'blank':  load_sprite("assets/sprites/blank.png"),
        'player': load_sprite("assets/sprites/at.png"),
        'bobcat': load_sprite("assets/sprites/image_not_found.png"),
        'wolf':   load_sprite("assets/sprites/image_not_found.png"),
        'wall':   load_sprite("assets/sprites/bush.png"),
        'grass0': load_sprite("assets/sprites/grass0.png"),
        'grass1': load_sprite("assets/sprites/grass1.png"),
        'grass2': load_sprite("assets/sprites/grass2.png"),
        'grass3': load_sprite("assets/sprites/grass3.png"),
        'grass4': load_sprite("assets/sprites/grass4.png"),
        'image_not_found_path': load_sprite("assets/sprites/image_not_found.png")
    }

    constants = {
        'map_width': map_width,
        'map_height': map_height,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'start_hp': start_hp,
        'start_def': start_def,
        'start_power': start_power,
        'max_monsters_per_room': max_monsters_per_room,
        'tile_size': tile_size,
        'sprites': sprites
    }

    return constants

# screen, tile_sheet, player, entities, game_map = get_game_variables(constants)
def get_game_variables():
    screen: pygame.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    constants = get_constants()
    
    fighter_component = Fighter(hp=constants['start_hp'], defense=constants['start_def'], power=constants['start_power'])
    player = Entity(x=constants['map_width'] // 2, y=constants['map_height'] // 2, name='player', sprite=constants['sprites'].get('player'), 
        render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]

    game_map = GameMap(constants['map_width'], constants['map_height'], constants['sprites'])
    game_map.make_map(player, entities, constants['max_monsters_per_room'])

    return screen, player, entities, game_map

