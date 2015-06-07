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
        self.name = ""
        self.type = 0
        self.color = WHITE
        self.x = 0  # x position
        self.y = 0  # y position
        self.moves = [[]]  # a list of paths which contain a list of moves
        self.abilities = {}

    def generate_dict(self):
        moves = []
        for move in moves:
            moves.append(move.generate_dict())
        abilities = []
 #       for ability in abilities:
 #           abilities.append(ability.generate_dict())
        dictionary = {
            'ID': self.ID,
            'name': self.name,
            'type': self.type,
            'color': self.color,
            'x': self.x,
            'y': self.y,
            'moves': moves,
            'abilities': abilities,
        }
        return dictionary

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
        self.fly = False  # when true, can fly over obstructions and friendly pieces

    def generate_dict(self):
        dictionary = {
            'x': self.x,
            'y': self.y,
            'fly': self.fly
        }
