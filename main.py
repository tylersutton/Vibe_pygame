import pygame

from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from loaders.initialize_new_game import get_game_variables
from render_functions import render_all



def main():
    pygame.init()
    
    screen, player, entities, game_map = get_game_variables()

    play_game(game_map, player, entities, screen)



def play_game(game_map, player, entities, screen):
    fov_radius = 8
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    
    clock = pygame.time.Clock()

    running = True
    while (running):
        #check events
        for event in pygame.event.get():
            action = handle_keys(event)
            if action.get("exit"):
                running = False
            elif "move" in action:
                move_x, move_y = action["move"]
                if not game_map.is_blocked(player.x + move_x, player.y + move_y):
                    player.move(move_x, move_y)
                    fov_recompute = True
        


        # TODO: process events

        # reset fov and render
        if fov_recompute:
            fov_map = recompute_fov(game_map, player.x, player.y, fov_radius)

        fov_recompute = False
        
        render_all(game_map, fov_map, fov_radius, player, entities, screen)
        print(int(clock.get_fps()))
        clock.tick(30)

    
        


if __name__ == '__main__':
    main()