from random import randint

import pygame

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from entity import Entity
from item_functions import cast_confuse, cast_fireball, cast_lightning, heal
from map_objects.tile import Tile
from render_functions import RenderOrder
from ui.elements.game_messages import Message

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.init_tiles()
        self.bg_tiles = self.init_bg_tiles()

    def init_tiles(self):
        tiles = [[Tile('blank', False) for y in range(self.height)] for x in range(self.width)]
        return tiles
    
    def init_bg_tiles(self):
        bg_tiles = [[('grass0', False) for y in range(self.height)] for x in range(self.width)]
        grass_img = 'grass0'
        for y in range(self.height):
            for x in range(self.width):
                rand_num = randint(0, 4)
                if rand_num == 0:
                    grass_img = 'grass0'
                if rand_num == 1:
                    grass_img = 'grass1'
                if rand_num == 2:
                    grass_img = 'grass2'
                if rand_num == 3:
                    grass_img = 'grass3'
                if rand_num == 4:
                    grass_img = 'grass4'
                bg_tiles[x][y] = Tile(grass_img, False)
        return bg_tiles

    def make_map(self, player, entities, max_monsters_per_room, max_items_per_room):
        fill_percentage = 45
        map_bound = 3
        spawn_radius = 3
        path_half_width = (self.width + self.height) // 16

        for y in range(self.height):
            for x in range(self.width):
                if randint(0,100) <= fill_percentage:
                    self.tiles[x][y].blocked = True
                    self.tiles[x][y].block_sight = True
                elif x < map_bound or y < map_bound or x >= self.width-map_bound or y >= self.height-map_bound:
                    self.tiles[x][y].blocked = True
                    self.tiles[x][y].block_sight = True
                
                #temp addition to see map
                self.tiles[x][y].explored = False
        
        #open_side = randint(0,3)
        open_side = 3
        print(open_side)
        y_mid = self.height // 2
        x_mid = self.width // 2
        y_bot = 0
        y_top = 0
        x_bot = 0
        x_top = 0

        if open_side == 0: #right side
            x_bot = self.width - (path_half_width*2)
            x_top = self.width
            y_bot = y_mid - path_half_width
            y_top = y_mid + path_half_width
        if open_side == 1: #top side
            x_bot = x_mid - path_half_width
            x_top = x_mid + path_half_width
            y_bot = 0
            y_top = (path_half_width*2)
        if open_side == 2: #left side
            x_bot = 0
            x_top = path_half_width*2
            y_bot = y_mid - path_half_width
            y_top = y_mid + path_half_width

        if open_side == 3: #bottom side
            x_bot = x_mid - path_half_width
            x_top = x_mid + path_half_width
            y_bot = self.height - (path_half_width*2)
            y_top = self.height
        
        for y in range(y_bot, y_top):
            for x in range(x_bot, x_top):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

        for x in range(12):
            self.smooth_tiles()
        
        self.fill_map_sprites()

        (player.x, player.y) = self.find_spawn(spawn_radius)
        self.place_entities(entities, max_monsters_per_room, max_items_per_room)


    def find_spawn(self, radius):
        spawn_found = False
        while (not spawn_found):
            spawn_found = True
            new_x = randint(radius,self.width-radius)
            new_y = randint(radius,self.height-radius)
            for x in range( new_x - radius, new_x + radius):
                for y in range(new_y - radius, new_y + radius):
                    x_dist = new_x - x
                    y_dist = new_y - y
                    if(((x_dist*x_dist) + (y_dist*y_dist)) <= (radius*radius)) and self.tiles[x][y].blocked:
                        spawn_found = False
                    if not spawn_found:
                        break
                if not spawn_found:
                    break

        return (new_x, new_y)

    def fill_map_sprites(self):
        for y in range(self.height):
            for x in range(self.width):
                wall = self.tiles[x][y].blocked
                if wall:
                    self.tiles[x][y].tile_type = 'wall'
                
    def smooth_tiles(self):
        temp = [[Tile('blank', False) for y in range(self.height)] for x in range(self.width)]
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                if (neighbors > 4):
                    temp[x][y].blocked = True
                    temp[x][y].block_sight = True
                elif (neighbors < 4):
                    temp[x][y].blocked = False
                    temp[x][y].block_sight = False
                else:
                    temp[x][y].blocked = self.tiles[x][y].blocked
                    temp[x][y].block_sight = self.tiles[x][y].block_sight
        self.tiles = temp
 

    def count_neighbors(self, x, y):
        num_neighbors = 0
        for j in range (y-1, y+2):
            for i in range(x-1, x+2):
                if (i >= 0 and j >= 0 and j < self.height and i < self.width):
                    if ((j != y or i != x) and self.tiles[i][j].blocked and self.tiles[i][j].block_sight):
                        num_neighbors = num_neighbors + 1
                else:
                    num_neighbors = num_neighbors + 1
        return num_neighbors

    def place_entities(self, entities, max_monsters_per_room, max_items_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)
        for _ in range(number_of_monsters):
            # Choose a random location in the room
            # radius of 1 because enemies will just walk around anyway
            (x, y) = self.find_spawn(1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 50:
                    fighter_comp = Fighter(hp=10, defense=0, power=3)
                    ai_comp = BasicMonster()
                    monster = Entity(x, y, 'Bobcat', 'bobcat', 'bones',
                        blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_comp, ai=ai_comp)
                else:
                    fighter_comp = Fighter(hp=16, defense=1, power=4)
                    ai_comp = BasicMonster()
                    monster = Entity(x, y, 'Wolf', 'wolf', 'bones',
                        blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_comp, ai=ai_comp)

                entities.append(monster)
        
        for _ in range(number_of_items):
            x, y = self.find_spawn(1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_chance = randint(0, 100)
                
                if item_chance < 70:
                    item_component = Item(use_function=heal, amount=4)
                    item = Entity(x, y, 'Healing Potion', 'healing_potion', render_order=RenderOrder.ITEM,
                        item=item_component)
                    entities.append(item)
                elif item_chance < 80:
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', pygame.Color('cyan')),
                                          damage=12, radius=3)
                    item = Entity(x, y, 'Fireball Scroll', 'fireball_scroll', render_order=RenderOrder.ITEM,
                        item=item_component)
                    entities.append(item)
                elif item_chance < 90:
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', pygame.Color('cyan')))
                    item = Entity(x, y, 'Confusion Scroll', 'confusion_scroll', render_order=RenderOrder.ITEM,
                        item=item_component)
                    entities.append(item)
                else:
                    item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, 'Lightning Scroll', 'lightning_scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                    entities.append(item)

    def is_blocked(self, x, y):
        if self.out_of_bounds(x, y) or self.tiles[x][y].blocked:
            return True

        return False

    def out_of_bounds(self, x, y):
        return not ((0 <= x < self.width) and (0 <= y < self.height))
