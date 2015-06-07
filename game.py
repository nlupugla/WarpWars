from constants import *

class Game:
    """
    This represents a game.

    It Contains the canonical copy of the game's state.
    """

    def __init__(self):
        """
        Set up a game with default conditions.

        :return: an initialized Game object
        """
        self.turn = 0  # 1 on the first turn, 2 on the second turn...
        self.active_color = WHITE  # color currently taking its turn
        self.phase = QUEEN_PHASE  # int indicating current phase
        self.units = {} # list of units in play
        self.board = [[]] # 2d array of board elements
        self.players = []  # list of players in the game
        self.over = False  # set to true when the game ends
        pass

    def next_turn(self):
        """
        Advance to next turn.

        Increment turn counter and update active player
        :return: nothing
        """
        self.turn += 1
        self.active_color = int(not self.active_color)

    def next_phase(self):
        """
        Advance phase to next one in order.

        :return: nothing
        """
        # draw and empty warp at the end of clean up phase
        if self.phase == CLEAN_UP_PHASE:
            inactive_player = self.players[not self.active_color]
            inactive_player.warp = 0
            inactive_player.draw()
        self.phase = (self.phase + 1)%3

    def move(self, unit_ID, x, y):
        """
        Move a unit.

        :param unit_ID: Unique numeric identifier of the unit to move
        :param x: x position of move
        :param y: y position of move
        :return: If the move was legal, return True, otherwise False
        """
        # check that the destination is on the board
        if x + 1 > BOARD_LENGTH or y + 1 > BOARD_HEIGHT: return False

        legality = False
        unit = self.units[unit_ID]
        for path in unit.moves:
            x_tracker = unit.x
            y_tracker = unit.y
            for move in path:
                # if something is at the destination, the move is illegal
                x_tracker += move.x
                y_tracker += move.y
                tile_value = self.board[x_tracker][y_tracker]
                if (tile_value == OBSTRUCTION and not move.fly) or \
                        (tile_value == self.active_color and not move.fly): break


        return True

    def deploy(self, unit_name, destination):
        """
        Deploys a unit onto the board.

        :param unit_name: Name of the unit to deploy
        :param x: x position of move
        :param y: y position of move
        :return:
        """
        return True
        pass

    def state(self):
        """
        Return the entire game state.

        :return: Text in json format containing all of the game's data
        """
        json = "Look at the llamas!"
        return json

    def generate_dict(self):
        """
        Create a dictionary object containing all of the game's data to be sent to the client.

        :return: a dictionary formatted to be an argument for json.dumps
        """

        units = []
        for unit in self.units:
            units.append(unit.generate_dict())
        players = []
#        for player in self.players:
#            players.append(player.generate_dict())
        dictionary = {
            'turn': self.turn,
            'active_color': self.active_color,
            'phase': self.phase,
            'units': units,
            'players': players,
            'over': self.over,
        }
        return dictionary
