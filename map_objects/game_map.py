from random import randint, shuffle

import pygame

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from entity import Entity
from graph import makeMapGraph
from item_functions import cast_confuse, cast_fireball, cast_lightning, heal
from map_objects.room import Room
from map_objects.tile import Tile
from render_functions import RenderOrder
from ui.elements.game_messages import Message
from utility import line, line_directions

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.init_tiles()
        self.bg_tiles = self.init_bg_tiles()
        self.rooms = []

    def init_tiles(self):
        tiles = [[Tile('wall', True) for y in range(self.height)] for x in range(self.width)]
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


    def make_map(self, player, entities, map_constants, map_graph_constants):
        map_border = 3
        fill_percentage = 35
        smooth_amount = 10
        min_graph_width, min_graph_height, max_graph_width, max_graph_height = map_graph_constants
        min_room_size, max_room_size, max_monsters_per_room, max_items_per_room = map_constants

        graph_width = randint(min_graph_width, max_graph_width)
        graph_height = randint(min_graph_height, max_graph_height)

        self.rooms = [None for _ in range(graph_width*graph_height)]
        map_graph = makeMapGraph(graph_width, graph_height)
        sector_width = self.width//graph_width
        sector_height = self.height//graph_height
        for y in range(graph_height):
            for x in range(graph_width):
                if map_graph.isNode(y*map_graph.width + x):
                    room_width = randint(min_room_size, min(max_room_size, sector_width-1))
                    room_height = randint(min_room_size, min(max_room_size, sector_height-1))
                    room_start_x = x*sector_width + randint(0, sector_width - room_width)
                    room_start_x = max(map_border, min(room_start_x, self.width - room_width - map_border))
                    room_start_y = y*sector_height + randint(0, sector_height - room_height)
                    room_start_y = max(map_border, min(room_start_y, self.height - room_height - map_border))
                
                    room = Room(pygame.Rect(((room_start_x, room_start_y)), (room_width, room_height)))
                    self.rooms[y*graph_width + x] = room
                    self.create_room(room)
        
        self.random_fill_rooms(fill_percentage)
        self.smooth_rooms(smooth_amount)

        # create paths between rooms based on graph edges
        for u, v, _ in map_graph.graph:
            self.create_tunnel(self.rooms[u], self.rooms[v])
        player.x = 0
        player.y = 0
        while (player.x, player.y) == (0, 0):
            room_num = randint(0, len(self.rooms)-1)
            if self.rooms[room_num]:
                player.x, player.y = self.rooms[room_num].center()

        self.smooth_rooms(smooth_amount)
        self.random_fill_rooms(5)

        self.fill_map_sprites()

        self.place_entities(entities, max_monsters_per_room, max_items_per_room)

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def random_fill_rooms(self, fill_percentage):
        for room in self.rooms:
            if room:
                for y in range(room.y1, room.y2):
                    for x in range(room.x1, room.x2):
                        chance = randint(0,100)
                        if chance < fill_percentage:
                            self.tiles[x][y].blocked = True
                            self.tiles[x][y].block_sight = True

    def smooth_rooms(self, smooth_amount):
        temp = [[Tile('wall', True) for y in range(self.height)] for x in range(self.width)]
        for y in range(0, self.height):
            for x in range(0, self.width):
                temp[x][y].blocked = self.tiles[x][y].blocked
                temp[x][y].block_sight = self.tiles[x][y].block_sight
        for room in self.rooms:
            if room:
                for _ in range(smooth_amount):
                    for y in range(room.y1, room.y2):
                        for x in range(room.x1, room.x2):
                            neighbors = self.count_neighbors(x, y)
                            if neighbors > 4:
                                temp[x][y].blocked = True
                                temp[x][y].block_sight = True
                            elif neighbors < 4:
                                temp[x][y].blocked = False
                                temp[x][y].block_sight = False
                            else:
                                temp[x][y].blocked = self.tiles[x][y].blocked
                                temp[x][y].block_sight = self.tiles[x][y].block_sight
        self.tiles = temp

    def count_neighbors(self, x, y):
        num_neighbors = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if (i >= 0 and j >= 0 and j < self.height and i < self.width):
                    if ((j != y or i != x) and self.tiles[i][j].blocked and self.tiles[i][j].block_sight):
                        num_neighbors = num_neighbors + 1
                else:
                    num_neighbors = num_neighbors + 1
        return num_neighbors


    def create_tunnel(self, room1, room2):
        x1, y1 = room1.center()
        x2, y2 = room2.center()
        for j in range(-1, 2):
            for i in range(-1, 2):
                path = line_directions(x1+i, y1+j, x2+i, y2+j)
                x = x1+i
                y = y1+j
                for dx, dy in path:
                    x += dx
                    y += dy
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].block_sight = False

    def find_spawn(self, room):
        found = False
        while not found:
            print('we good')
            x = randint(room.x1, room.x2)
            y = randint(room.y1, room.y2)
            if not self.is_blocked(x, y):
                return (x, y)

    def fill_map_sprites(self):
        for y in range(self.height):
            for x in range(self.width):
                wall = self.tiles[x][y].blocked
                if not wall:
                    self.tiles[x][y].tile_type = 'blank'
                

    def place_entities(self, entities, max_monsters_per_room, max_items_per_room):
        # Get a random number of monsters
        for room in self.rooms:
            if room is not None:
                number_of_monsters = randint(0, max_monsters_per_room)
                number_of_items = randint(0, max_items_per_room)
                for _ in range(number_of_monsters):
                    # Choose a random location in the room
                    # radius of 1 because enemies will just walk around anyway
                    x, y = self.find_spawn(room)

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
                    x, y = self.find_spawn(room)
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
