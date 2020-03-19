from game_states import GameStates
from render_functions import RenderOrder
from ui.elements.game_messages import Message

def kill_player(player):
    player.name = player.name + '(dead)'
    player.sprite_type = player.dead_sprite_type
    return Message('You died!'), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()))
    
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = monster.name + '(dead)'
    monster.render_order = RenderOrder.CORPSE
    monster.sprite_type = monster.dead_sprite_type

    return death_message