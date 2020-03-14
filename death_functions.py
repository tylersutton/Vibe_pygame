from game_states import GameStates
from render_functions import RenderOrder

def kill_player(player):
    player.name = player.name + '(dead)'
    player.sprite = player.dead_sprite
    return 'You died!', GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = '{0} is dead!'.format(monster.name.capitalize())
    
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = monster.name + '(dead)'
    monster.render_order = RenderOrder.CORPSE
    monster.sprite = monster.dead_sprite

    return death_message