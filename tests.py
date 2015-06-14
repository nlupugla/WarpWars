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
    return_game.deploy(WARPLING_TYPE, 5, 5)
    return_game.active_color = BLACK
    return_game.deploy(WARPLING_TYPE, 6, 6)
    return return_game

class GameTest(unittest.TestCase):

    def test_initialization(self):
        game = test_game()
        self.assertEqual(game.board[5][5], WHITE_TILE)
        self.assertEqual(game.board[6][6], BLACK_TILE)
        self.assertEqual(game.units[1].x, 5)
        self.assertEqual(game.units[2].x, 6)

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
        self.assertFalse(game.move(2, 6, 6)) # should be False because start location = end location
        self.assertFalse(game.move(1, 6, 6)) # should be False because this move is out of range
        self.assertEqual(game.board[5][5], WHITE_TILE)
        self.assertEqual(game.board[6][6], BLACK_TILE)
        self.assertTrue(game.move(1, 5, 6))
        self.assertEqual(game.board[5][6], WHITE_TILE)
        self.assertTrue(game.move(2, 5, 6))
        self.assertEqual(game.board[5][6], BLACK_TILE)
        print game.state()

if __name__ == '__main__':
    unittest.main()
