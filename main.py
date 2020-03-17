x = 100
y = 100
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

import pygame
import pygame_gui

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from loaders.initialize_new_game import get_game_variables
from profiler import profile
from render_functions import render_all
from ui.elements.game_messages import Message

# @profile
def main():
    pygame.init()
    
    screen, manager, screen_health_bar, entity_info, player, entities, game_map, map_surf, camera = get_game_variables()

    play_game(game_map, map_surf, camera, player, entities, screen, manager, screen_health_bar, entity_info)


def play_game(game_map, map_surf, camera, player, entities, screen, manager, screen_health_bar, entity_info):
    fov_radius = 8
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    
    clock = pygame.time.Clock()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    running = True
    while (running):
        time_delta = clock.tick(60)/1000.0
        
        #check events
        for event in pygame.event.get():
            action = handle_keys(event, game_state)
            
            move = action.get("move")
            pickup = action.get("pickup")
            show_inventory = action.get("show_inventory")
            drop_inventory = action.get("drop_inventory")
            inventory_index = action.get("inventory_index")
            fullscreen = action.get("fullscreen")
            
            if action.get("exit"):
                if game_state == GameStates.SHOW_INVENTORY:
                    game_state = previous_game_state
                else:
                    running = False

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
                    player_turn_results.extend(player.inventory.use(item))
                elif game_state == GameStates.DROP_INVENTORY:
                    player_turn_results.extend(player.inventory.drop_item(item))

            for player_turn_result in player_turn_results:
                message = player_turn_result.get('message')
                dead_entity = player_turn_result.get('dead')
                item_added = player_turn_result.get('item_added')
                item_consumed = player_turn_result.get('consumed')
                item_dropped = player_turn_result.get('item_dropped')

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

        # TODO: process events

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