class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, name, sprite, blocks=False):
        self.x = x
        self.y = y
        self.name = name
        self.sprite = sprite
        self.blocks = blocks

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy