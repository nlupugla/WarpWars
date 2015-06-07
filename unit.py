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
        self.ID = Unit.n_deployed
        Unit.n_deployed += 1
        self.name = ""
        self.type = 0
        self.color = WHITE
        self.x = 0  # x position
        self.y = 0  # y position
        self.moves = [[]]  # a list of paths which contain a list of moves
        self.abilities = {}

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
