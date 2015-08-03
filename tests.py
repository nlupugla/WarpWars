import unittest

from game import Game
from card import Card
from player import Player
from graph import Graph
from constants import *
from card_dictionary import CARD_DICTIONARY

def make_game():
    game = Game()
    game.players = [Player(WHITE), Player(BLACK, True)]
    for player in game.players:
        player.warp = 1000
        player.add_card(WARPLING_TYPE, BOARD_LENGTH*START_ZONE_HEIGHT)
        player.add_card(ROOK_TYPE, 2)
        player.add_card(QUEEN_TYPE, 1)
        player.add_card(KING_TYPE, 1)
        player.add_card(GOLD_GENERAL_TYPE, 2)
        player.add_card(SILVER_GENERAL_TYPE, 2)

        game.active_color = player.color
        game.deploy(WARPLING_TYPE, player.color, 1, player.adjust(0), False)
        game.deploy(ROOK_TYPE, player.color, 3, player.adjust(0), False)
        game.deploy(KING_TYPE, player.color, 4, player.adjust(0), False)
        game.deploy(QUEEN_TYPE, player.color, 5, player.adjust(0), False)
        game.deploy(ROOK_TYPE, player.color, 6, player.adjust(0), False)
        game.deploy(WARPLING_TYPE, player.color, 8, player.adjust(0), False)

        game.deploy(WARPLING_TYPE, player.color, 0, player.adjust(1), False)
        game.deploy(WARPLING_TYPE, player.color, 2, player.adjust(1), False)
        game.deploy(SILVER_GENERAL_TYPE, player.color, 3, player.adjust(1), False)
        game.deploy(GOLD_GENERAL_TYPE, player.color, 4, player.adjust(1), False)
        game.deploy(GOLD_GENERAL_TYPE, player.color, 5, player.adjust(1), False)
        game.deploy(SILVER_GENERAL_TYPE, player.color, 6, player.adjust(1), False)
        game.deploy(WARPLING_TYPE, player.color, 7, player.adjust(1), False)
        game.deploy(WARPLING_TYPE, player.color, 9, player.adjust(1), False)

        for x in range(BOARD_LENGTH):
            if x not in {0, 2, 7, 9}:
                game.deploy(WARPLING_TYPE, player.color, x, player.adjust(2), False)
        player.warp = 1

        player.remove_card(WARPLING_TYPE)
        player.remove_card(KING_TYPE)
        player.remove_card(QUEEN_TYPE)
        player.remove_card(GOLD_GENERAL_TYPE)
        player.remove_card(SILVER_GENERAL_TYPE)

        player.add_card(SUPER_PAWN_TYPE, 6)
        player.add_card(LANCE_TYPE, 5)
        player.add_card(KNIGHT_TYPE, 4)
        player.add_card(BISHOP_TYPE, 4)
        player.add_card(ROOK_TYPE, 3)
        player.add_card(PROMOTED_BISHOP_TYPE, 2)
        player.add_card(PROMOTED_ROOK_TYPE, 1)

    game.turn = 1
    game.active_color = STARTING_PLAYER
    return game

def test_game():
    return_game = Game()
    return_game.players = [Player(WHITE), Player(BLACK)]
    for player in return_game.players:
        player.add_card(WARPLING_TYPE, BOARD_LENGTH*BOARD_HEIGHT)
    return_game.active_color = WHITE
    return_game.deploy(WARPLING_TYPE, WHITE, 5, 5, False)
    return_game.active_color = BLACK
    return_game.deploy(WARPLING_TYPE, BLACK, 6, 6, False)
    return_game.turn = 1
    return return_game

def checkers_game():
    # return a game with a checkers style arrangement of warplings.
    game = Game()
    game.players = [Player(WHITE), Player(BLACK, True)]
    for player in game.players:
        player.add_card(WARPLING_TYPE, BOARD_LENGTH*START_ZONE_HEIGHT)
        player.add_card(KNIGHT_TYPE, 7)
        player.add_card(BISHOP_TYPE, 7)
        player.add_card(ROOK_TYPE, 5)
        player.add_card(QUEEN_TYPE, 1)
        player.add_card(KING_TYPE, 1)

    game.active_color = game.players[0].color
    for x in range(BOARD_LENGTH):
        for y in range(START_ZONE_HEIGHT):
            if (x, y) == (BOARD_LENGTH/2, 0):
                game.deploy(KING_TYPE, game.active_color, x, y, False)
            elif (x % 2) == (y % 2):
                game.deploy(WARPLING_TYPE, game.players[0].color, x, y, False)

    game.active_color = game.players[1].color
    for x in range(BOARD_LENGTH):
        for y in range(BOARD_HEIGHT - START_ZONE_HEIGHT, BOARD_HEIGHT):
            if (x, y) == (BOARD_LENGTH/2, BOARD_HEIGHT - 1):
                game.deploy(KING_TYPE, game.active_color, x, y, False)
            elif x % 2 == (y - (BOARD_HEIGHT - START_ZONE_HEIGHT)) % 2:
                game.deploy(WARPLING_TYPE, game.players[1].color, x, y, False)

    game.active_color = STARTING_PLAYER
    game.turn = 1
    return game

def single_unit_game(unit_type):
    game = Game()
    game.players = [Player(WHITE), Player(BLACK)]
    game.players[0].add_card(unit_type, 1)
    game.players[0].warp = 100
    game.active_color = WHITE
    game.deploy(unit_type, WHITE, BOARD_LENGTH/2, BOARD_HEIGHT/2, False)
    return game

class GameTest(unittest.TestCase):

    def test_initialization(self):
        game = test_game()
        self.assertEqual(game.board[5][5], WHITE_TILE)
        self.assertEqual(game.board[6][6], BLACK_TILE)
        self.assertEqual(game.units[1].x, 5)
        self.assertEqual(game.units[2].x, 6)

        game = checkers_game()
        self.assertEqual(game.board[0][0], WHITE_TILE)
        self.assertEqual(game.board[9][1], WHITE_TILE)
        self.assertEqual(game.board[9][8], BLACK_TILE)
        self.assertEqual(len(game.units), 32)

        game = make_game()
        self.assertTrue(game.get_unit_by_position(8, 2) is not None)
        self.assertEqual(game.get_unit_by_position(5, 0).type, QUEEN_TYPE)

    def test_basic_movement(self):
        game = test_game()
        ID = game.state_ID
        game.active_color = BLACK
        """
        the following is left out for now because it assumed a different warpling move set.
        
        self.assertFalse(game.move(2, 6, 6))  # should be False because start location = end location
        game.active_color = WHITE
        self.assertFalse(game.move(1, 6, 6))  # should be False because this move is out of range
        self.assertEqual(ID, game.state_ID)
        self.assertEqual(game.board[5][5], WHITE_TILE)
        self.assertEqual(game.board[6][6], BLACK_TILE)
        game.active_color = WHITE
        self.assertTrue(game.move(1, 5, 6))
        self.assertLess(ID, game.state_ID)
        ID = game.state_ID
        self.assertEqual(game.board[5][6], WHITE_TILE)
        game.active_color = BLACK
        self.assertTrue(game.move(2, 5, 6))
        self.assertLess(ID, game.state_ID)
        self.assertEqual(game.board[5][6], BLACK_TILE)
        """

    def test_advanced_movement(self):
        game = checkers_game()
        game.active_color = WHITE
        game.players[WHITE].warp = 100
        game.deploy(BISHOP_TYPE, WHITE, 2, 2)
        bishop = game.get_unit_by_position(2, 2)
        self.assertTrue(game.move(bishop.ID, 4, 4))

class UnitTest(unittest.TestCase):  # The Unit in UnitTest is for the Unit class

    def setUp(self):
        self.warpling = CARD_DICTIONARY[WARPLING_TYPE].copy()
        self.knight = CARD_DICTIONARY[KNIGHT_TYPE].copy()
        self.bishop = CARD_DICTIONARY[BISHOP_TYPE].copy()
        self.rook = CARD_DICTIONARY[ROOK_TYPE].copy()
        self.king = CARD_DICTIONARY[KING_TYPE].copy()
        self.queen = CARD_DICTIONARY[QUEEN_TYPE].copy()

    def test_bishop(self):
        game = single_unit_game(BISHOP_TYPE)
        x0 = BOARD_LENGTH/2
        y0 = BOARD_HEIGHT/2
        bishop = game.get_unit_by_position(x0, y0)
        self.assertTrue(game.move(bishop.ID, x0 + 1, y0 + 1))
        self.assertTrue(game.move(bishop.ID, x0 - 1, y0 - 1))
        self.assertFalse(game.move(bishop.ID, x0, y0 - 1))
        self.assertTrue(game.move(bishop.ID, x0, y0))
        self.assertTrue(game.move(bishop.ID, x0 - 3, y0 + 3))

    def test_rook(self):
        game = single_unit_game(ROOK_TYPE)
        x0 = BOARD_LENGTH/2
        y0 = BOARD_HEIGHT/2
        rook = game.get_unit_by_position(x0, y0)
        self.assertTrue(game.move(rook.ID, x0 + 1, y0))
        self.assertTrue(game.move(rook.ID, x0 - 2, y0))
        self.assertTrue(game.move(rook.ID, x0 - 2, y0 + 3))
        self.assertFalse(game.move(rook.ID, x0, y0))


class GraphTest(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.add_new_node(0, 0)
        self.graph.add_new_node(-1, 1)
        self.graph.add_new_node(0, 1)
        self.graph.add_new_node(1,1)
        self.graph.add_new_node(-1, 2)
        self.graph.add_new_node(0, 2)
        self.graph.add_new_node(1,2)
        self.graph.connect_adjacent_nodes()

    def test_set_up(self):
        my_graph = self.graph
        self.assertTrue(my_graph.find_node_by_position(0, 0) is not None)
        self.assertTrue(my_graph.find_node_by_position(1, 1) is not None)
        self.assertEquals(my_graph.num_nodes(), 7)
        self.assertEquals(my_graph.num_edges(), 8)
        self.assertTrue(my_graph.are_neighbours(my_graph.find_node_by_position(0, 0), my_graph.find_node_by_position(0, 1)))
        self.assertFalse(my_graph.are_neighbours(my_graph.find_node_by_position(0, 0), my_graph.find_node_by_position(1, 1)))

    def test_copy(self):
        my_graph = self.graph
        my_graph.connect_all_to(my_graph.find_node_by_position(0,0))
        self.assertEquals(my_graph.num_nodes(), 7)
        self.assertEquals(my_graph.num_edges(), 13)

        my_new_graph = my_graph.copy()
        self.assertEquals(my_new_graph.num_nodes(), 7)
        self.assertEquals(my_new_graph.num_edges(), 13)
        for node in my_graph.mapping:
            for other_node in my_graph.mapping:
                copy_of_node = my_new_graph.find_node_by_ID(node.ID)
                copy_of_other_node = my_new_graph.find_node_by_ID(other_node.ID)
                if my_graph.are_neighbours(node, other_node):
                    self.assertTrue(my_new_graph.are_neighbours(copy_of_node, copy_of_other_node))

    def test_traversal_cost(self):
        my_graph = self.graph
        self.assertEqual(my_graph.traversal_cost(my_graph.find_node_by_position(1, 1), my_graph.find_node_by_position(-1, 1)), 2)
        self.assertEqual(my_graph.traversal_cost(my_graph.find_node_by_position(0, 0), my_graph.find_node_by_position(1, 2)), 3)
        self.assertEqual(my_graph.traversal_cost(my_graph.find_node_by_position(0, 1), my_graph.find_node_by_position(0, 1)), 0)
        my_graph.block_node(my_graph.find_node_by_position(-1, 1))
        my_graph.block_node(my_graph.find_node_by_position(0, 2))
        self.assertEqual(my_graph.traversal_cost(my_graph.find_node_by_position(0, 0), my_graph.find_node_by_position(-1, 2)), BLOCKED)

class AbilityTest(unittest.TestCase):

    def test_barrier(self):
        game = single_unit_game(KING_TYPE)
        king_ID = 1
        game.use_ability(king_ID, 'barrier', x=2, y=2)
        self.assertEqual(game.get_unit_by_position(2, 2).type, BARRIER_TYPE)
        print game.state()

if __name__ == '__main__':
    unittest.main()
