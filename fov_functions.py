import math

def initialize_fov(game_map):
    # None == unprocessed
    # True/False == visibility
    return [[False for y in range(game_map.height)] for x in range(game_map.width)]

def recompute_fov(game_map, player_x, player_y, radius):
    fov_map = initialize_fov(game_map)
    
    for i in range(0,360):
        x = math.sin(i*0.01745)
        y = math.cos(i*0.01745)
        do_fov(game_map, fov_map, x, y, player_x, player_y, radius)

    return fov_map

def do_fov(game_map, fov_map, x, y, player_x, player_y, radius):
    ox = player_x + 0.5
    oy = player_y + 0.5

    for j in range(0, radius):
        if not (0 <= int(ox) < game_map.width and 0 <= int(oy) < game_map.height):
            return
        fov_map[int(ox)][int(oy)] = True
        if game_map.tiles[int(ox)][int(oy)].block_sight:
            return
        ox += x
        oy += y