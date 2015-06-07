from constants import *

STARTING_PLAYER = WHITE


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
        self.current_turn = 0  # 1 on the first turn, 2 on the second turn...
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
        self.crnt_turn += 1
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
        unit = self.units[unit_ID]

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
