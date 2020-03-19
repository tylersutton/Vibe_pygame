import pygame
import pygame_gui

from game_states import GameStates


def handle_keys(event, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(event)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(event)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(event)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(event)
    return {}

def handle_player_turn_keys(event):
    if event.type == pygame.KEYDOWN:
        button = event.key
        # movement keys
        if button == pygame.K_UP or button == pygame.K_k:
            return {"move": (0, -1)}
        elif button == pygame.K_DOWN or button == pygame.K_j:
            return {"move": (0, 1)}
        elif button == pygame.K_LEFT or button == pygame.K_h:
            return {"move": (-1, 0)}
        elif button == pygame.K_RIGHT or button == pygame.K_l:
            return {"move": (1, 0)}
        elif button == pygame.K_y:
            return {"move": (-1, -1)}
        elif button == pygame.K_u:
            return {"move": (1, -1)}
        elif button == pygame.K_b:
            return {"move": (-1, 1)}
        elif button == pygame.K_n:
            return {"move": (1, 1)}
        elif button == pygame.K_z:
            return {"move": (0, 0)}

        if button == pygame.K_g:
            return {'pickup': True}

        elif button == pygame.K_i:
            return {'show_inventory': True}

        elif button == pygame.K_d:
            return {'drop_inventory': True}

        if button == pygame.K_ESCAPE:
            return {"exit": True}

        mods = pygame.key.get_pressed()
        if button == pygame.K_RETURN and mods[pygame.K_RALT]:
            # Alt+Enter: toggle fullscreen
            return {"fullscreen": True}

    return {}

def handle_inventory_keys(event):
    if event.type == pygame.KEYDOWN:
        button = event.key
        index = button - ord('a')
        
        if index >= 0:
            return {"inventory_index": index}
        
        mods = pygame.key.get_pressed()
        if button == pygame.K_RETURN and mods[pygame.K_RALT]:
            # Alt+Enter: toggle fullscreen
            return {"fullscreen": True}
        if button == pygame.K_ESCAPE:
            return {"exit": True}
    return {}

def handle_main_menu(event, main_menu):
    if event.type == pygame.KEYDOWN:
        button = event.key
        if button == pygame.K_a:
            return {'new_game': True}
        elif button == pygame.K_b:
            return {'load_game': True}
        elif button == pygame.K_c or button == pygame.K_ESCAPE:
            return {'exit': True}
    elif event.type == pygame.USEREVENT:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == main_menu.new_game_button:
                return {'new_game': True}
            elif event.ui_element == main_menu.load_game_button:
                return {'load_game': True}
            elif event.ui_element == main_menu.exit_button:
                return {'exit': True}

    return {}

def handle_targeting_keys(event):
    if event.type == pygame.KEYDOWN:
        button = event.key
        if button == pygame.K_ESCAPE:
            return {"exit": True}
    return {}

def handle_mouse(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        (x, y) = pygame.mouse.get_pos()
        (l, m, r) = pygame.mouse.get_pressed()
        if l:
            return {"left_click": (x, y)}
        elif r:
            return {"right_click": (x, y)}
        elif m:
            return {"middle_click": (x, y)}
    return {}

def handle_inventory_buttons(event, game_state, inventory_menu):
    if event.type == pygame.USEREVENT and game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if inventory_menu:
                for index in range(0, len(inventory_menu.buttons)):
                    if event.ui_element == inventory_menu.buttons[index]:
                        return {'inventory_index': index}
    return {}


def handle_player_dead_keys(event):
    if event.type == pygame.KEYDOWN:
        button = event.key

        if button == pygame.K_i:
            return {'show_inventory': True}

        mods = pygame.key.get_pressed()
        if button == pygame.K_RETURN and mods[pygame.K_RALT]:
            # Alt+Enter: toggle fullscreen
            return {"fullscreen": True}
        if button == pygame.K_ESCAPE:
            return {"exit": True}
    return {}