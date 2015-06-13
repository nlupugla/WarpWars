from constants import *
from graph import Graph

class Unit:
    """
    Units move on the board and have abilities.

    Each unit has an x and y position on the board, a list of legal moves, a list of abilities, a name, and a unique
    identifier to distinguish it from others of the same name.
    """

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
        self.graph = Graph()
        self.abilities = {}

    def clone_unit(self, unit):
        """
        Copy constructor to make silly Python happy

        :param unit: unit to copy
        :return: a new unit with exactly the same values as the input
        """
        self.ID = unit.ID
        self.name = unit.name
        self.type = unit.type
        self.color = unit.color
        self.x = unit.x
        self.y = unit.y
        self.moves = unit.moves
        self.abilities = unit.abilities

    def generate_dict(self):
        """
        Create a dictionary object containing all of the unit's data to be sent to the client.

        :return: a dictionary formatted to be an argument for json.dumps
        """
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
