from constants import *

class Unit:
    """
    Units move on the board and have abilities.

    Each unit has an x and y position on the board, a list of legal moves, a list of abilities, a name, and a unique
    identifier to distinguish it from others of the same name.
    """
    n_deployed = 0
    def __init__(self):
        """
        Create a unit with default values

        :return: an initialized unit object
        """
        self.ID = 0
        self.name = 0
        self.x = 0  # x position
        self.y = 0  # y position
        self.moves = [()] # list of 2-tuples enumerating potential moves
        self.abilities = {}

