from json import dumps

from constants import *
from card_dictionary import CARD_DICTIONARY

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
        self.board = [] # 2d array of board elements
        for x in range(BOARD_LENGTH):
            self.board.append([EMPTY_TILE]*BOARD_HEIGHT)
        self.players = []  # list of players in the game
        self.n_units_deployed = 0 # total number of units deployed in the game
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

    def place(self, unit, x, y):
        """
        Place a unit at the specified coordinates

        :param unit: the unit to place
        :param x: x position
        :param y: y position
        :return: nothing
        """
        # TODO: Do something about taking?
        unit.x = x
        unit.y = y
        if self.board[x][y] == (not self.active_color):
            self.take(x, y)
        self.board[x][y] = self.active_color
        self.units[unit.ID] = unit

    def take(self, x, y):
        for unit in self.units:
            if unit.x == x and unit.y == y:
                self.units.remove(unit)
                return True
        return False

    def move(self, unit_ID, x, y):
        """
        Move a unit.

        :param unit_ID: Unique numeric identifier of the unit to move
        :param x: x position of move
        :param y: y position of move
        :return: If the move was legal, return True, otherwise False
        """
        legality = False
        # check that the destination is on the board
        if x + 1 > BOARD_LENGTH or y + 1 > BOARD_HEIGHT: return legality
        if x < 0 or y < 0: return legality

        # grab unit by ID
        unit = self.units[unit_ID]

        # loop through all possible paths available to the unit
        for path in unit.moves:
            x_tracker = unit.x
            y_tracker = unit.y
            # if one of the moves in the path is the destination, and you can get there legally, move the piece
            for move in path:
                x_tracker += move.x
                y_tracker += move.y
                tile_value = self.board[x_tracker][y_tracker]
                # if something is at the destination, the move is illegal
                if (tile_value == OBSTRUCTION and not move.fly) or \
                        (tile_value == self.active_color and not move.fly): break
                if x_tracker == x and y_tracker == y:
                    self.place(unit, x, y)
                    legality = True
                    return legality

    def deploy(self, card_ID, x, y):
        """
        Deploys a unit onto the board.

        :param card_ID: unique identifier of card to be deployed as unit
        :param x: x position of deployment destination
        :param y: y position of deployment destination
        :return:
        """
        legality = False
        #grab card by ID
        player = self.players[self.active_color]
        card = player.palette[card_ID]
        # check legality
        if x + 1 > BOARD_LENGTH or y + 1 > BOARD_HEIGHT: return legality
        if x < 0 or y < 0: return legality
        if self.board[x][y] != EMPTY_TILE: return legality
        # if card.cost > player.warp: return legality
        # TODO: Implement a cap on the number of cards of the same type you can play?

        unit = CARD_DICTIONARY[card]
        unit.color = self.active_color
        self.n_units_deployed += 1
        unit.ID = self.n_units_deployed
        self.place(unit, x, y)
        return True

    def state(self):
        """
        Return the entire game state.

        :return: Text in json format containing all of the game's data
        """
        game_dict = self.generate_dict()
        json = dumps(game_dict)
        return json

    def generate_dict(self):
        """
        Create a dictionary object containing all of the game's data to be sent to the client.

        :return: a dictionary formatted to be an argument for json.dumps
        """

        units = []
        for unit in self.units:
            units.append(self.units[unit].generate_dict())
        players = []
#        for player in self.players:
#            players.append(player.generate_dict())
        dictionary = {
            'turn': self.turn,
            'active_color': self.active_color,
            'phase': self.phase,
            'units': units,
            'players': players,
            'n_units_deployed': self.n_units_deployed,
            'over': self.over,
        }
        return dictionary
