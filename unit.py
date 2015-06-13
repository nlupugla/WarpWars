from constants import *
from graph import Graph
from copy import deepcopy

class Unit:
    """
    Units move on the board and have abilities.

    Each unit has an x and y position on the board, a list of legal moves, a list of abilities, a name, and a unique
    identifier to distinguish it from others of the same name.
    """

    def __init__(self, unit=None):
        """
        Create a unit with default values if no argument given or a deep copy of the input unit if an argument is given.

        :param unit: a unit to copy.
        :return: an initialized unit object
        """
        if unit is None:
            self.ID = 0 # unique identifier of every unit in play
            self.name = "" # name of the unit
            self.type = 0 # number specifying unit's type, eg: WARPLING_TYPE
            self.color = WHITE # number specifying to which player the unit belongs
            self.x = 0  # x position
            self.y = 0  # y position
            self.moves = Graph() # graph specifying the movement of the unit
            self.abilities = {} # a list of all the abilities the unit owns
        else:
            self = deepcopy(unit)

    def generate_dict(self):
        """
        Create a dictionary object containing all of the unit's data to be sent to the client.

        :return: a dictionary formatted to be an argument for json.dumps
        """
        moves = self.moves.generate_dict()
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
