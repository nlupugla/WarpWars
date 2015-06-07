from constants import *

class Move:
    """
    A relative move from one tile to another

    Move objects hold the x and y position relative to a starting location and whether the moving can piece can "fly"
    over obstacles.
    """

    def __init__(self, direction=-1, magnitude=1, fly=False):
        """
        Create a move from the input values.

        :param direction: direction of the move; accepted values are NORTH, EAST, SOUTH, WEST
        :param magnitude: magnitude of the move in the given direction
        :param fly: when True, the move ignores obstructions
        :return: a Move object specifying a new location relative to the starting point
        """
        if direction == -1:
            self.x = 0
            self.y = 0
        if direction == NORTH:
            self.x = 0
            self.y = magnitude
        elif direction == EAST:
            self.x = magnitude
            self.y = 0
        elif direction == SOUTH:
            self.x = 0
            self.y = -1*magnitude
        elif direction == WEST:
            self.x = -1*magnitude
            self.y = 0
        self.fly = fly

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
