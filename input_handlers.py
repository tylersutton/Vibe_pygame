import pygame

from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    return {}

def handle_player_turn_keys(key):
    if key.type == pygame.KEYDOWN:
        button = key.key
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

    elif key.type == pygame.QUIT:
        return {"exit": True}
    return {}

def handle_player_dead_keys(key):
    if key.type == pygame.KEYDOWN:
        button = key.key

        if button == pygame.K_i:
            return {'show_inventory': True}

        mods = pygame.key.get_pressed()
        if button == pygame.K_RETURN and mods[pygame.K_RALT]:
            # Alt+Enter: toggle fullscreen
            return {"fullscreen": True}
        if button == pygame.K_ESCAPE:
            return {"exit": True}

    return {}

def handle_inventory_keys(key):
    if key.type == pygame.KEYDOWN:
        button = key.key
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