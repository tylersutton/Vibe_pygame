import math

from components.ai import BasicMonster
from components.fighter import Fighter
from render_functions import RenderOrder
from components.item import Item
from components.inventory import Inventory
from utility import astar

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x: int, y: int, name: str, sprite_type: str, dead_sprite_type: str = None,
                 blocks: bool = False, render_order: int = RenderOrder.CORPSE, fighter: Fighter = None,
                 ai: BasicMonster = None, item: Item = None, inventory: Inventory = None):
        self.x = x
        self.y = y
        self.name = name
        self.sprite_type = sprite_type
        self.dead_sprite_type = dead_sprite_type
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self
        
        if self.inventory:
            self.inventory.owner = self

    def copy(self):
        new_entity = Entity(self.x, self.y, self.name, self.sprite_type, self.dead_sprite_type, self.blocks, 
                            self.render_order, self.fighter, self.ai, self.item, self.inventory)
        return new_entity

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                    get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)
    
    def move_astar(self, target_x, target_y, game_map, entities):
        path = astar(game_map, (self.x, self.y), (target_x, target_y))
        if path:
            new_x, new_y = path[1]

            if not (game_map.is_blocked(new_x, new_y) or
                    get_blocking_entities_at_location(entities, new_x, new_y)):
                self.move(new_x - self.x, new_y - self.y)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None