import pygame

from components.fighter import Fighter
from components.inventory import Inventory
from entity import Entity
from map_objects.camera import Camera
from map_objects.game_map import GameMap
from map_objects.map_surface import MapSurface
from render_functions import load_sprite, RenderOrder
from ui.elements.entity_info import EntityInfo
from ui.elements.game_messages import MessageLog
from ui.health_bar import HealthBar
from ui.manager import UIManager

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

def get_constants():
    title = 'Vibe'
    
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT

    map_width = 100
    map_height = 75
    map_on_screen_x = 160
    map_on_screen_y = 0
    map_on_screen_width = screen_width - map_on_screen_x
    map_on_screen_height = screen_height - map_on_screen_y - 120
    map_rect = pygame.Rect((map_on_screen_x, map_on_screen_y), (map_on_screen_width, map_on_screen_height))

    camera_width = 42
    camera_height = 24
    # camera_width = 56
    # camera_height = 32

    health_bar_bg_color = (50, 50, 50)
    health_bar_fg_color = (255, 0, 0)
    health_bar_x = 5
    health_bar_y = 10
    health_bar_width = 150
    health_bar_height = 30
    health_bar_rect = pygame.Rect((health_bar_x, health_bar_y), (health_bar_width, health_bar_height))


    entity_info_x = map_on_screen_x
    entity_info_y = 480
    entity_info_width = screen_width - entity_info_x
    entity_info_height = 16
    entity_info_rect = pygame.Rect((entity_info_x, entity_info_y), (entity_info_width, entity_info_height))

    message_log_x = 0
    message_log_y = 500
    message_log_width = screen_width - message_log_x
    message_log_height = screen_height - message_log_y
    message_log_rect = pygame.Rect((message_log_x, message_log_y), (message_log_width, message_log_height))

    main_menu_rect = pygame.Rect((0,0), (screen_width, screen_height))

    inventory_menu_x = map_on_screen_x + 10
    inventory_menu_y = map_on_screen_y + 10
    inventory_menu_width = map_on_screen_width - 20
    inventory_menu_height = map_on_screen_height - 20
    inventory_menu_rect = pygame.Rect((inventory_menu_x, inventory_menu_y),
                                        (inventory_menu_width, inventory_menu_height))

    start_hp = 100
    start_def = 2
    start_power = 5
    start_inventory = 20

    max_monsters_per_room = 20
    max_items_per_room = 200

    tile_width = map_on_screen_width // camera_width
    tile_height = map_on_screen_height // camera_height
    tile_size = (tile_width, tile_height)
    
    theme1 = "assets/themes/theme1.json"
    
    sprites = get_sprites(tile_size)

    constants = {
        'title': title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'map_width': map_width,
        'map_height': map_height,
        'map_rect': map_rect,
        'camera_width': camera_width,
        'camera_height': camera_height,
        'health_bar_bg_color': health_bar_bg_color,
        'health_bar_fg_color': health_bar_fg_color,
        'health_bar_rect': health_bar_rect,
        'entity_info_rect': entity_info_rect,
        'message_log_rect': message_log_rect,
        'main_menu_rect': main_menu_rect,
        'inventory_menu_rect': inventory_menu_rect,
        'start_hp': start_hp,
        'start_def': start_def,
        'start_power': start_power,
        'start_inventory': start_inventory,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'tile_width': tile_width,
        'tile_height': tile_height,
        'theme1': theme1,
        'sprites': sprites
    }

    return constants

def get_sprites(tile_size):
    sprites = {
        'blank':  load_sprite("assets/sprites/blank.png", tile_size),
        'player': load_sprite("assets/sprites/at.png", tile_size),
        'bobcat': load_sprite("assets/sprites/bobcat.png", tile_size),
        'wolf':   load_sprite("assets/sprites/wolf.png", tile_size),
        'bones':  load_sprite("assets/sprites/bones.png", tile_size),
        'wall':   load_sprite("assets/sprites/bush.png", tile_size),
        'grass0': load_sprite("assets/sprites/grass0.png", tile_size),
        'grass1': load_sprite("assets/sprites/grass1.png", tile_size),
        'grass2': load_sprite("assets/sprites/grass2.png", tile_size),
        'grass3': load_sprite("assets/sprites/grass3.png", tile_size),
        'grass4': load_sprite("assets/sprites/grass4.png", tile_size),
        'healing_potion': load_sprite("assets/sprites/healing_potion.png", tile_size),
        'lightning_scroll': load_sprite("assets/sprites/lightning_scroll.png", tile_size),
        'fireball_scroll': load_sprite("assets/sprites/fireball_scroll.png", tile_size),
        'confusion_scroll': load_sprite("assets/sprites/confusion_scroll.png", tile_size),
        'image_not_found_path': load_sprite("assets/sprites/image_not_found.png", tile_size)
    }
    return sprites

# screen, tile_sheet, player, entities, game_map = get_game_variables(constants)
def get_game_variables():
    screen: pygame.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    constants = get_constants()
    pygame.display.set_caption(constants['title'])
    
    manager = UIManager(width=constants['screen_width'], height=constants['screen_height'],
        main_menu_rect=constants['main_menu_rect'],
        message_log_rect=constants['message_log_rect'], theme=constants['theme1'])

    fighter_component = Fighter(hp=constants['start_hp'], defense=constants['start_def'], power=constants['start_power'])
    inventory_component = Inventory(constants['start_inventory'])
    player = Entity(x=constants['map_width'] // 2, y=constants['map_height'] // 2, name='player',
        sprite_type='player', dead_sprite_type='bones',
        render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component)
    
    entities = [player]

    screen_health_bar = HealthBar(name=player.name, hp=player.fighter.hp, max_hp=player.fighter.max_hp,
        bg_color=constants['health_bar_bg_color'], fg_color=constants['health_bar_fg_color'],
        rect=constants['health_bar_rect'])

    entity_info = EntityInfo(constants['entity_info_rect'])

    map_surf = MapSurface(constants['map_rect'], constants['sprites'])

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(player, entities, constants['max_monsters_per_room'],
            constants['max_items_per_room'])

    camera = Camera(game_map, player, constants['camera_width'], constants['camera_height'])

    return screen, manager, screen_health_bar, entity_info, player, entities, game_map, map_surf, camera

