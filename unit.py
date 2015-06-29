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
        Create a unit with default values if no argument given or a deep copy of the input unit if an argument is given.

        :return: an initialized unit object
        """
        self.ID = 0  # unique identifier of every unit in play
        self.name = ""  # name of the unit
        self.type = 0  # number specifying unit's type, eg: WARPLING_TYPE
        self.color = WHITE  # number specifying to which player the unit belongs
        self.cost = 0  # amount of warp required to play the unit
        self.x = -1  # x position
        self.y = -1  # y position
        self.moves = Graph()  # graph specifying the movement of the unit
        self.abilities = {}  # a list of all the abilities the unit owns

    def copy(self):
        """
        Return a copy of the unit.

        :return: a unit with the same values as the caller.
        """
        unit = Unit()
        unit.ID = self.ID
        unit.name = self.name
        unit.type = self.type
        unit.color = self.color
        unit.cost = self.cost
        unit.x = self.x
        unit.y = self.y
        unit.moves = self.moves.copy()
        unit.abilities = self.abilities
        return unit

    def generate_dict(self):
        """
        Create a dictionary object containing all of the unit's data to be sent to the client.

        :return: a dictionary formatted to be an argument for json.dumps
        """
        abilities = []
 #       for ability in abilities:
 #           abilities.append(ability.generate_dict())
        dictionary = {
            'ID': self.ID,
            'name': self.name,
            'type': self.type,
            'color': self.color,
            'cost': self.cost,
            'x': self.x,
            'y': self.y,
            'abilities': abilities,
        }
        return dictionary
