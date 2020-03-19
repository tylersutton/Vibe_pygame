x = 100
y = 100
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

import pygame

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_inventory_buttons, handle_keys, handle_main_menu, handle_mouse
from loaders.data_loaders import load_game, save_game
from loaders.initialize_new_game import get_game_variables
from profiler import profile
from render_functions import render_all, get_map_coords
from ui.elements.game_messages import Message
from ui.elements.menus import MainMenu

# @profile
def main():
    pygame.init()

    game_running = True
    show_main_menu = True
    show_load_error_message = False
    game_state = GameStates.PLAYERS_TURN
    screen, manager, screen_health_bar, entity_info, player, entities, game_map, map_surf, camera = get_game_variables()

    manager.init_main_menu()

    clock = pygame.time.Clock()

    while (game_running):
        time_delta = clock.tick(60)/1000.0
        if show_main_menu:
            for event in pygame.event.get():
                manager.gui.process_events(event)

                if event.type == pygame.QUIT:
                    game_running = False
                
                action = handle_main_menu(event, manager.main_menu)

                new_game = action.get('new_game')
                load_saved_game = action.get('load_game')
                exit_game = action.get('exit')
                
                if new_game:
                    game_state = GameStates.PLAYERS_TURN
                    show_main_menu = False

                elif load_saved_game:
                    try:
                        player, entities, game_map, camera, game_state = load_game()
                        show_main_menu = False
                    except FileNotFoundError:
                        show_load_error_message = True

                elif exit_game:
                    break
            manager.update(time_delta)
            manager.gui.draw_ui(screen)
            pygame.display.flip()
        else:
            manager.kill_main_menu()
            if not manager.message_log:
                manager.init_message_log()
            play_game(game_map, map_surf, camera, player, entities, screen, manager, screen_health_bar, entity_info, game_state)
            manager.kill_message_log()
            manager.init_main_menu()
            show_main_menu = True


def play_game(game_map, map_surf, camera, player, entities, screen, manager, screen_health_bar, entity_info, game_state):
    fov_radius = 8
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    
    clock = pygame.time.Clock()

    previous_game_state = game_state

    targeting_item = None

    running = True
    while (running):
        time_delta = clock.tick(60)/1000.0
        
        #check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(player, entities, game_map, camera, game_state)
                running = False
            
            manager.gui.process_events(event)

            action = handle_keys(event, game_state)
            mouse_action = handle_mouse(event)
            button_action = handle_inventory_buttons(event, game_state, manager.inventory_menu)
            move = action.get("move")
            pickup = action.get("pickup")
            show_inventory = action.get("show_inventory")
            drop_inventory = action.get("drop_inventory")
            inventory_index = action.get("inventory_index")
            if inventory_index is None:
                inventory_index = button_action.get("inventory_index")
            fullscreen = action.get("fullscreen")

            left_click = mouse_action.get('left_click')
            right_click = mouse_action.get('right_click')

            player_turn_results = []

            if move and game_state == GameStates.PLAYERS_TURN:
                dx, dy = action["move"]
                dest_x = player.x + dx
                dest_y = player.y + dy
                if not game_map.is_blocked(dest_x, dest_y):
                    target = get_blocking_entities_at_location(entities, dest_x, dest_y)
                    if target:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)
                    else:
                        player.move(dx, dy)
                        fov_recompute = True
                game_state = GameStates.ENEMY_TURN
        
            elif pickup and game_state == GameStates.PLAYERS_TURN:
                for entity in entities:
                    if entity.item and entity.x == player.x and entity.y == player.y:
                        pickup_results = player.inventory.add_item(entity)
                        player_turn_results.extend(pickup_results)

                        break
                else:
                    manager.add_to_message_log(Message('There is nothing here to pick up.'))

            elif show_inventory:
                previous_game_state = game_state
                game_state = GameStates.SHOW_INVENTORY

            elif drop_inventory:
                previous_game_state = game_state
                game_state = GameStates.DROP_INVENTORY

            if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                    player.inventory.items):
                item = player.inventory.items[inventory_index]
                if game_state == GameStates.SHOW_INVENTORY:
                    player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
                elif game_state == GameStates.DROP_INVENTORY:
                    player_turn_results.extend(player.inventory.drop_item(item))

            if game_state == GameStates.TARGETING:
                if left_click:
                    target_x, target_y = left_click
                    target_x, target_y = get_map_coords(target_x, target_y, map_surf.width // camera.width, 
                                                        map_surf.height // camera.height, camera, map_surf)

                    item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                    player_turn_results.extend(item_use_results)
                elif right_click:
                    player_turn_results.append({'targeting_cancelled': True})

            if action.get("exit"):
                if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                    game_state = previous_game_state
                elif game_state == GameStates.TARGETING:
                    player_turn_results.append({'targeting_cancelled': True})
                else:
                    save_game(player, entities, game_map, camera, game_state)
                    running = False

            for player_turn_result in player_turn_results:
                message = player_turn_result.get('message')
                dead_entity = player_turn_result.get('dead')
                item_added = player_turn_result.get('item_added')
                item_consumed = player_turn_result.get('consumed')
                item_dropped = player_turn_result.get('item_dropped')
                targeting = player_turn_result.get('targeting')
                targeting_cancelled = player_turn_result.get('targeting_cancelled')

                if message:
                    manager.add_to_message_log(message)

                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                        game_state = GameStates.PLAYER_DEAD
                    else:
                        message = kill_monster(dead_entity)
                    manager.add_to_message_log(message)
                
                if item_added:
                    entities.remove(item_added)
                    game_state = GameStates.ENEMY_TURN

                if item_consumed:
                    game_state = GameStates.ENEMY_TURN

                if item_dropped:
                    entities.append(item_dropped)
                    game_state = GameStates.ENEMY_TURN

                if targeting:
                    previous_game_state = GameStates.PLAYERS_TURN
                    game_state = GameStates.TARGETING

                    targeting_item = targeting

                    manager.add_to_message_log(targeting_item.item.targeting_message)

                if targeting_cancelled:
                    game_state = previous_game_state

                    manager.add_to_message_log(Message('Targeting cancelled'))

            if game_state == GameStates.ENEMY_TURN:
                for entity in entities:
                    if entity.ai:
                        enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                        for enemy_turn_result in enemy_turn_results:
                            message = enemy_turn_result.get('message')
                            dead_entity = enemy_turn_result.get('dead')

                            if message:
                                manager.add_to_message_log(message)
                            if dead_entity:
                                if dead_entity == player:
                                    message, game_state = kill_player(dead_entity)
                                else:
                                    message = kill_monster(dead_entity)

                                manager.message_log.add_message(message)

                                if game_state == GameStates.PLAYER_DEAD:
                                    break
                        if game_state == GameStates.PLAYER_DEAD:
                            break
                else:
                    game_state = GameStates.PLAYERS_TURN

        # TO DO: process events

        # reset fov and render
        if fov_recompute:
            fov_map = recompute_fov(game_map, player.x, player.y, fov_radius)

        fov_recompute = False

        manager.update(time_delta)

        camera.update()

        render_all(game_map, map_surf, camera, fov_map, fov_radius, player, entities, screen, manager, screen_health_bar, entity_info, game_state)

        # print(int(clock.get_fps()))
    
        


if __name__ == '__main__':
    main()