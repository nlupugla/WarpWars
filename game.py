from json import dumps

from constants import *
from card_dictionary import CARD_DICTIONARY
from ability_dictionary import ABILITY_DICTIONARY

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
        self.phase = MOVE_PHASE  # int indicating current phase
        self.units = {}  # list of units in play key: unit_ID -> item: unit
        self.board = []  # 2d array of board elements
        for x in range(BOARD_LENGTH):
            self.board.append([EMPTY_TILE]*BOARD_HEIGHT)
        self.players = []  # list of players in the game
        self.n_units_deployed = 0  # total number of units deployed in the game
        self.state_ID = 0  # total number different states
        self.over = False  # set to true when the game ends

    def next_turn(self):
        """
        Advance to next turn.

        Increment turn counter and update active player
        :return: nothing
        """
        self.turn += 1
        self.phase = MOVE_PHASE
        self.active_color = int(not self.active_color)
        self.players[self.active_color].warp = (self.turn + self.turn % 2)/2  # Hearthstone style resources
        self.state_ID += 1

    def next_phase(self):
        """
        Advance phase to next one in order.

        :return: nothing
        """
        self.phase = (self.phase + 1) % 3
        self.state_ID += 1

    def move_is_legal(self, unit_ID, x, y):
        """
        Return whether moving a unit the specified coordinates is legal or not given the current board position.

        :param unit_ID: unique identifier of the unit to move
        :param x: x coordinate of destination.
        :param y: y coordinate of destination.
        :return: True if the move is legal, False otherwise.
        """
        # TODO: Do we want more specific return values or error messages?
        # The unit must belong to the active player.
        if self.units[unit_ID].color != self.active_color:
            return False
        # The destination must not be off the board.
        if x + 1 > BOARD_LENGTH or y + 1 > BOARD_HEIGHT:
            return False
        if x < 0 or y < 0:
            return False
        # Grab the unit by ID.
        unit = self.units[unit_ID]
        movement = unit.moves
        # The destination must not be a unit of the same color or an obstruction.
        if self.board[x][y] == unit.color or self.board[x][y] == OBSTRUCTION:
            return False
        # The destination must be different from the starting location.
        if (x, y) == (unit.x, unit.y):
            return False
        start_node = movement.find_node_by_position(unit.x, unit.y)
        end_node = movement.find_node_by_position(x, y)
        # The destination must be within the unit's range.
        if end_node is None:
            return False
        # Now if the path to any node in the destination's neighbourhood is not blocked, the move is legal.
        for node in movement.neighbourhood(end_node):
            if movement.traversal_cost(start_node, node) < BLOCKED:
                return True
        # If they are all blocked, the move is illegal.
        return False

    def list_legal_moves(self, unit_ID):
        """
        Return the list of legal moves for the given unit.

        :param unit_ID: unique identifier of the unit.
        :return: a 2D list where (legal_moves[i][0], legal_moves[i][1]) is the (x, y) coordinate of the ith legal move.
        """
        legal_moves = []
        for x in range(BOARD_LENGTH):
            for y in range(BOARD_HEIGHT):
                if self.move_is_legal(unit_ID, x, y):
                    legal_moves.append([x, y])
        return legal_moves

    def move(self, unit_ID, x, y):
        """
        Attempt to move a unit to the specified location.

        :param unit_ID: Unique numeric identifier of the unit to move.
        :param x: x coordinate of move.
        :param y: y coordinate of move.
        :return: If the move was legal, return True, otherwise False.
        """
        legal = self.move_is_legal(unit_ID, x, y)
        if not legal:
            return False
        unit = self.units[unit_ID]
        self.place(unit, x, y)
        self.next_phase()
        self.state_ID += 1
        return True

    def place(self, unit, x, y, deploy=False):
        """
        Place a unit at the specified destination.

        Put a unit at the given position, take if necessary, then update the movement graph of all pieces. Note that,
        unlike Game.move, this method does not check legality.
        :param unit: the unit to place.
        :param x: x coordinate of the destination.
        :param y: y coordinate of the destination.
        :param deploy: When True, the placement is for a deploy, which means the unit has no starting position.
        :return: nothing.
        """
        # take any piece at the destination
        self.take(x, y)
        # update board
        if not deploy:
            self.board[unit.x][unit.y] = EMPTY_TILE
        self.board[x][y] = unit.color
        # update graph position
        movement = unit.moves
        for node in movement.mapping:
            if deploy:
                node.x += x
                node.y += y
            else:
                node.x += x - unit.x
                node.y += y - unit.y
        # update unit position
        unit.x = x
        unit.y = y
        self.update_movements()
        self.state_ID += 1

    def update_movements(self):
        """
        Update the movement graph of every unit in play to reflect the current board.

        :return: nothing.
        """
        for key in self.units:
            unit = self.units[key]
            movement = unit.moves
            # unblock nodes on the first pass
            for node in movement.mapping:
                x = node.x
                y = node.y
                if (0 <= x < BOARD_LENGTH) and (0 <= y < BOARD_HEIGHT):
                    if self.board[x][y] == EMPTY_TILE or (x, y) == (unit.x, unit.y):
                        movement.unblock_position(x, y)
            # block nodes on the second pass
            for node in movement.mapping:
                x = node.x
                y = node.y
                if (0 <= x < BOARD_LENGTH) and (0 <= y < BOARD_HEIGHT):
                    if self.board[x][y] != EMPTY_TILE and (x, y) != (unit.x, unit.y):
                        movement.block_position(x, y)

    def take(self, x, y):
        """
        Take a unit at the given position out of the game.

        :param x: x coordinate of position.
        :param y: y coordinate of position.
        :return: True if there is a unit at the given position, False otherwise.
        """
        # TODO: Rename to destroy?
        for key in self.units:
            if self.units[key].x == x and self.units[key].y == y:
                del self.units[key]
                self.board[x][y] = EMPTY_TILE
                self.update_movements()
                self.state_ID += 1
                return True
        return False

    def deploy_is_legal(self, unit_type, color, x, y, legal=True):
        """
        Return whether deploying a card to the specified destination is legal or not.

        :param unit_type: number specifying the type of the unit to be deployed, eg: WARPLING_TYPE.
        :param color: the color of the unit being deployed, WHITE or BLACK.
        :param x: x coordinate of deployment destination.
        :param y: y coordinate of deployment destination.
        :param legal: When True, the unit must be deployed legally, according to the rules.
        :return: True if the deploy is legal, False otherwise.
        """
        # The destination must not be off the board.
        if x + 1 > BOARD_LENGTH or y + 1 > BOARD_HEIGHT:
            return False
        if x < 0 or y < 0:
            return False
        if legal:
            player = self.players[self.active_color]
            # The color of the unit being deployed must match the active color.
            if color != self.active_color:
                return False
            unit = self.get_unit_by_position(x, y)
            if unit is None or unit.type != WARPLING_TYPE or unit.color != player.color:
                return False
            # The player must have enough warp.
            if player.palette[unit_type].cost > player.warp:
                return False
            # The player must have enough cards in their palette of the card type.
            if player.palette[unit_type].current_amount < 1:
                return False
        return True

    def deploy(self, unit_type, color, x, y, legal=True):
        """
        Deploy a unit onto the board.

        :param unit_type: number specifying the type of the unit to be deployed, eg: WARPLING_TYPE.
        :param color: the color of the unit being deployed, WHITE or BLACK.
        :param x: x coordinate of deployment destination.
        :param y: y coordinate of deployment destination.
        :param legal: When True, the unit must be deployed legally, according to the rules.
        :return: True if the deploy was successful, False otherwise.
        """
        if not self.deploy_is_legal(unit_type, color, x, y, legal):
            return False
        player = self.players[self.active_color]
        if legal:
            # decrease the player's warp by the cost of the unit.
            player.warp -= player.palette[unit_type].cost
            # decrement number of units of the type in the player's palette.
            player.palette[unit_type].current_amount -= 1
        # initialize unit
        unit = CARD_DICTIONARY[unit_type].copy()
        if self.players[color].flipped:
            unit.moves.flip(0)
        unit.color = self.active_color
        self.n_units_deployed += 1
        unit.ID = self.n_units_deployed
        # put the unit in play
        self.units[unit.ID] = unit
        deploy = True
        self.place(unit, x, y, deploy)
        self.state_ID += 1
        return True

    def use_ability_is_legal(self, unit_ID, ability_name, **kwargs):
        pass

    def list_legal_use_abilities(self, unit_ID, ability_name, **kwargs):
        pass

    def use_ability(self, unit_ID, ability_name, **kwargs):
        """
        Use a unit's ability.

        The game uses ability_name as a key to locate and execute some code which functions as a units ability. The
        design space for abilities should be as open as possible, so this function takes an arbitrary name-identified
        list of arguments. Currently used key words are:
        x - an int specifying the x-coordinate of the ability's target.
        y - an int specifying the y-coordinate of the ability's target.
        :param ability_name: a string matching the name of one of the abilities in ABILITY_DICTIONARY
        :param kwargs: key word arguments
        :return: True of the ability was used successfully, false otherwise.
        """
        ABILITY_DICTIONARY[ability_name](self, **kwargs)
        self.state_ID += 1


    def get_unit_by_position(self, x, y):
        """
        Return the unit in the game at the specified location.

        :param x: x coordinate.
        :param y: y coordinate.
        :return: the specified unit if one exists at the location, None otherwise.
        """
        for unit_ID in self.units:
            unit = self.units[unit_ID]
            if (unit.x, unit.y) == (x, y):
                return unit

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
        for key in self.units:
            unit = self.units[key]
            unit_dict = unit.generate_dict()
            unit_dict['legal_moves'] = self.list_legal_moves(unit.ID)
            units.append(unit_dict)
        players = []
        for player in self.players:
            players.append(player.generate_dict())
        dictionary = {
            'turn': self.turn,
            'active_color': self.active_color,
            'phase': self.phase,
            'units': units,
            'players': players,
            'n_units_deployed': self.n_units_deployed,
            'state_ID': self.state_ID,
            'over': self.over,
        }
        return dictionary
