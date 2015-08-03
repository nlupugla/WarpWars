from constants import *

def barrier(game, x, y):
    game.deploy(BARRIER_TYPE, game.active_color, x, y, False)

ABILITY_DICTIONARY = {
    'barrier': barrier
}
