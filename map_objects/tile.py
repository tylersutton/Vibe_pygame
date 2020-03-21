class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, tile_type, blocked, block_sight=None):
        self.tile_type = tile_type
        self.blocked = blocked
        self.explored = True # temp for now
        
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight