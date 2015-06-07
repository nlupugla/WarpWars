from constants import *

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
        """
        Create a dictionary object containing all of the move's data to be sent to the client.

        :return: a dictionary formatted to be an argument for json.dumps
        """
        dictionary = {
            'x': self.x,
            'y': self.y,
            'fly': self.fly
        }
        return dictionary
