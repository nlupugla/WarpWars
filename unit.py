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
        self.moves = [[]] # a list of paths which contain a list of moves
        self.abilities = {}

class Move:
    """
    A relative move from one tile to another

    Move objects hold the x and y position relative to a starting location and whether the moving can piece can "fly"
    over obstacles.
    """

    def __init__(self):
        """
        Create a move with default values

        :return: an initialized move object
        """
        self.x = 0
        self.y = 0
        self.fly = False # when true, can fly over obstructions and friendly pieces

