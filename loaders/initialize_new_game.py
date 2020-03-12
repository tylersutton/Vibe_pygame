import pygame
import pygame_gui

from components.fighter import Fighter
from entity import Entity
from map_objects.game_map import GameMap
from render_functions import load_sprite, RenderOrder
from ui.elements.game_messages import MessageLog
from ui.health_bar import HealthBar
from ui.manager import UIManager

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

def get_constants():
    title = 'Vibe'
    
    map_width = 50
    map_height = 30
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT

    health_bar_bg_color = (50, 50, 50)
    health_bar_fg_color = (255, 0, 0)
    health_bar_x = 10
    health_bar_y = 10
    health_bar_width = 100
    health_bar_height = 10

    message_log_x = 30
    message_log_y = 500
    message_log_width = 400
    message_log_height = 100

    start_hp = 30
    start_def = 2
    start_power = 5

    max_monsters_per_room = 10

    tile_width = screen_width // map_width
    tile_height = screen_height // map_height
    tile_size = (tile_width, tile_height)
    sprites = {
        'blank':  load_sprite("assets/sprites/blank.png", tile_size),
        'player': load_sprite("assets/sprites/at.png", tile_size),
        'bobcat': load_sprite("assets/sprites/bobcat.png", tile_size),
        'wolf':   load_sprite("assets/sprites/wolf.png", tile_size),
        'wall':   load_sprite("assets/sprites/bush.png", tile_size),
        'grass0': load_sprite("assets/sprites/grass0.png", tile_size),
        'grass1': load_sprite("assets/sprites/grass1.png", tile_size),
        'grass2': load_sprite("assets/sprites/grass2.png", tile_size),
        'grass3': load_sprite("assets/sprites/grass3.png", tile_size),
        'grass4': load_sprite("assets/sprites/grass4.png", tile_size),
        'image_not_found_path': load_sprite("assets/sprites/image_not_found.png", tile_size)
    }

    constants = {
        'title': title,
        'map_width': map_width,
        'map_height': map_height,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'health_bar_bg_color': health_bar_bg_color,
        'health_bar_fg_color': health_bar_fg_color,
        'health_bar_x': health_bar_x,
        'health_bar_y': health_bar_y,
        'health_bar_width': health_bar_width,
        'health_bar_height': health_bar_height,
        'message_log_x': message_log_x,
        'message_log_y': message_log_y,
        'message_log_width': message_log_width,
        'message_log_height': message_log_height,
        'start_hp': start_hp,
        'start_def': start_def,
        'start_power': start_power,
        'max_monsters_per_room': max_monsters_per_room,
        'tile_width': tile_width,
        'tile_height': tile_height,
        'sprites': sprites
    }

    return constants

# screen, tile_sheet, player, entities, game_map = get_game_variables(constants)
def get_game_variables():
    screen: pygame.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    constants = get_constants()
    pygame.display.set_caption(constants['title'])
    
    manager = UIManager(constants['screen_width'], constants['screen_height'])
    
    message_log = MessageLog(constants['message_log_x'], constants['message_log_y'],
        constants['message_log_width'], constants['message_log_height'], manager.gui)
    
    manager.init_message_log(message_log)
    
    fighter_component = Fighter(hp=constants['start_hp'], defense=constants['start_def'], power=constants['start_power'])
    player = Entity(x=constants['map_width'] // 2, y=constants['map_height'] // 2, name='player', sprite=constants['sprites'].get('player'), 
        render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]

    screen_health_bar = HealthBar(hp=player.fighter.hp, max_hp=player.fighter.max_hp, 
        bg_color=constants['health_bar_bg_color'], fg_color=constants['health_bar_fg_color'], 
        x=constants['health_bar_x'], y=constants['health_bar_y'],
        width=constants['health_bar_width'], height=constants['health_bar_height'])

    game_map = GameMap(constants['map_width'], constants['map_height'], constants['sprites'])
    game_map.make_map(player, entities, constants['max_monsters_per_room'])

    return screen, manager, screen_health_bar, player, entities, game_map

