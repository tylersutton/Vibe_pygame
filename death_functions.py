from game_states import GameStates
from render_functions import RenderOrder

def kill_player(player):
    return 'You died!', GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = '{0} is dead!'.format(monster.name.capitalize())
    
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message