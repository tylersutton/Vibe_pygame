import pygame

def handle_keys(key):
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

        if button == pygame.K_ESCAPE:
            return {"exit": True}

        mods = pygame.key.get_pressed()
        if button == pygame.K_RETURN and mods[pygame.K_RALT]:
            # Alt+Enter: toggle fullscreen
            return {"fullscreen": True}

    elif key.type == pygame.QUIT:
        return {"exit": True}
    return {}