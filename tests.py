import unittest

from game import Game
from unit import Unit
from player import Player
from graph import Graph
from constants import *
from card_dictionary import CARD_DICTIONARY

def test_game():
    return_game = Game()
    return_game.players = [Player(WHITE), Player(BLACK)]
    return_game.active_color = WHITE
    return_game.deploy(WARPLING_TYPE, 5, 5, False)
    return_game.active_color = BLACK
    return_game.deploy(WARPLING_TYPE, 6, 6, False)
    return return_game

def make_game():
    # return a game with a checkers style arrangement of warplings.
    game = Game()
    game.players = [Player(WHITE), Player(BLACK)]
    game.players[0].palette[WARPLING_TYPE] = BOARD_LENGTH*BOARD_HEIGHT
    game.active_color = game.players[0].color
    for x in range(BOARD_LENGTH):
        for y in range(START_ZONE_HEIGHT):
            if (x % 2) == (y % 2):
                game.deploy(WARPLING_TYPE, x, y, False)
    game.players[1].palette[WARPLING_TYPE] = BOARD_LENGTH*BOARD_HEIGHT
    game.active_color = game.players[1].color
    for x in range(BOARD_LENGTH):
        for y in range(BOARD_HEIGHT - START_ZONE_HEIGHT, BOARD_HEIGHT):
            if x % 2 == (y - (BOARD_HEIGHT - START_ZONE_HEIGHT)) % 2:
                game.deploy(WARPLING_TYPE, x, y, False)
    game.active_color = STARTING_PLAYER
    return game




class GameTest(unittest.TestCase):

    def test_initialization(self):
        game = test_game()
        self.assertEqual(game.board[5][5], WHITE_TILE)
        self.assertEqual(game.board[6][6], BLACK_TILE)
        self.assertEqual(game.units[1].x, 5)
        self.assertEqual(game.units[2].x, 6)

        game = make_game()
        self.assertEqual(game.board[0][0], WHITE_TILE)
        self.assertEqual(game.board[9][1], WHITE_TILE)
        self.assertEqual(game.board[9][8], BLACK_TILE)
        self.assertEqual(len(game.units), 30)

    def test_graph(self):
        my_graph = Graph()
        my_graph.add_new_node(0, 0)
        my_graph.add_new_node(-1, 1)
        my_graph.add_new_node(0, 1)
        my_graph.add_new_node(1,1)
        my_graph.add_new_node(-1, 2)
        my_graph.add_new_node(0, 2)
        my_graph.add_new_node(1,2)
        my_graph.connect_adjacent_nodes()

        self.assertTrue(my_graph.find_node_by_position(0, 0) is not None)
        self.assertTrue(my_graph.find_node_by_position(1, 1) is not None)
        self.assertEquals(my_graph.num_nodes(), 7)
        self.assertEquals(my_graph.num_edges(), 8)

        self.assertTrue(my_graph.are_neighbours(my_graph.find_node_by_position(0, 0), my_graph.find_node_by_position(0, 1)))
        self.assertFalse(my_graph.are_neighbours(my_graph.find_node_by_position(0, 0), my_graph.find_node_by_position(1, 1)))

        self.assertEqual(my_graph.traversal_cost(my_graph.find_node_by_position(1, 1), my_graph.find_node_by_position(-1, 1)), 2)
        self.assertEqual(my_graph.traversal_cost(my_graph.find_node_by_position(0, 0), my_graph.find_node_by_position(1, 2)), 3)
        self.assertEqual(my_graph.traversal_cost(my_graph.find_node_by_position(0, 1), my_graph.find_node_by_position(0, 1)), 0)
        my_graph.block_node(my_graph.find_node_by_position(-1, 1))
        my_graph.block_node(my_graph.find_node_by_position(0, 2))
        self.assertEqual(my_graph.traversal_cost(my_graph.find_node_by_position(0, 0), my_graph.find_node_by_position(-1, 2)), BLOCKED)

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

    def test_movement(self):
        game = test_game()
        ID = game.state_ID
        game.active_color = BLACK
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

if __name__ == '__main__':
    unittest.main()
