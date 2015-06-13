import unittest

from game import *
from unit import *
from player import *
from card_dictionary import *
from graph import *

def test_game():
    return_game = Game()
    player1 = Player(WHITE)
    player2 = Player(BLACK)
    return_game.players = [player1, player2]
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

if __name__ == '__main__':
    unittest.main()
"""
    # test that moving works as it should
    print not game.move(1, 6, 6) # should print true as this is out of range
    print game.board[6][6] == BLACK_TILE # should still be true
    game.move(1, 5, 6)
    print game.board[5][6] == WHITE_TILE
    game.move(1, 6, 6)
    print game.board[6][6] == WHITE_TILE
    print game.units
"""