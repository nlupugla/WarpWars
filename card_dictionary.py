import unit
from constants import *
from move import *
from graph import Graph
fly = True

knight = unit.Unit()
knight.moves = [
    [Move(NORTH, 2, fly), Move(EAST)],
    [Move(NORTH, 2, fly), Move(WEST)],
    [Move(EAST, 2, fly), Move(NORTH)],
    [Move(EAST, 2, fly), Move(SOUTH)],
    [Move(SOUTH, 2, fly), Move(EAST)],
    [Move(SOUTH, 2, fly), Move(WEST)],
    [Move(WEST, 2, fly), Move(NORTH)],
    [Move(WEST, 2, fly), Move(SOUTH)],
]
knight_graph = Graph()
knight_graph.add_new_node(0, 0)
knight_graph.add_new_node(1, 2)
knight_graph.add_new_node(-1, 2)
knight_graph.add_new_node(2, 1)
knight_graph.add_new_node(2, -1)
knight_graph.add_new_node(1, -2)
knight_graph.add_new_node(-1, -2)
knight_graph.add_new_node(-2, -1)
knight_graph.add_new_node(-2, 1)
knight_graph.connect_all_to(knight_graph.find_node_by_position(0, 0))
knight.type = KNIGHT_TYPE

warpling = unit.Unit()
warpling.moves = [
    [Move(NORTH)],
    [Move(EAST)],
    [Move(SOUTH)],
    [Move(WEST)]
]
warpling_graph = Graph()
warpling_graph.add_new_node(0, 0)
warpling_graph.add_new_node(1, 0)
warpling_graph.add_new_node(0, 1)
warpling_graph.add_new_node(-1, 0)
warpling_graph.add_new_node(0, -1)
warpling_graph.connect_adjacent_nodes()
warpling.type = WARPLING_TYPE

CARD_DICTIONARY = {
    'knight': knight,
    'warpling': warpling
}