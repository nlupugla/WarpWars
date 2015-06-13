from unit import Unit
from constants import WARPLING_TYPE, KNIGHT_TYPE
from graph import Graph

# TODO: Add in abilities

warpling = Unit()
warpling.moves = Graph()
warpling.moves.add_new_node(0, 0)
warpling.moves.add_new_node(1, 0)
warpling.moves.add_new_node(0, 1)
warpling.moves.add_new_node(-1, 0)
warpling.moves.add_new_node(0, -1)
warpling.moves.connect_adjacent_nodes()
warpling.type = WARPLING_TYPE

knight = Unit()
knight.moves = Graph()
knight.moves.add_new_node(0, 0)
knight.moves.add_new_node(1, 2)
knight.moves.add_new_node(-1, 2)
knight.moves.add_new_node(2, 1)
knight.moves.add_new_node(2, -1)
knight.moves.add_new_node(1, -2)
knight.moves.add_new_node(-1, -2)
knight.moves.add_new_node(-2, -1)
knight.moves.add_new_node(-2, 1)
knight.moves.connect_all_to(knight.moves.find_node_by_position(0, 0))
knight.type = KNIGHT_TYPE

CARD_DICTIONARY = {
    WARPLING_TYPE: warpling,
    KNIGHT_TYPE: knight,
}
