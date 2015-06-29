from unit import Unit
from constants import *
from graph import Graph

# TODO: Add in abilities

warpling = Unit()
warpling.type = WARPLING_TYPE
warpling.name = "Warpling"
warpling.cost = 0
warpling.moves = Graph()
warpling.moves.add_new_node(0, 0)
warpling.moves.add_new_node(1, 0)
warpling.moves.add_new_node(0, 1)
warpling.moves.add_new_node(-1, 0)
warpling.moves.add_new_node(0, -1)
warpling.moves.connect_adjacent_nodes()

knight = Unit()
knight.type = KNIGHT_TYPE
knight.name = "Knight"
knight.cost = 3
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

bishop = Unit()
bishop.type = BISHOP_TYPE
bishop.name = "Bishop"
bishop.cost = 3
bishop.moves = Graph()
for x in range(-BOARD_LENGTH, BOARD_LENGTH + 1):
    for y in range(-BOARD_HEIGHT, BOARD_HEIGHT + 1):
        if x == y or x == -y:
            bishop.moves.add_new_node(x, y)
bishop.moves.connect_diagonal_nodes()

rook = Unit()
rook.type = ROOK_TYPE
rook.name = "Rook"
rook.cost = 5
rook.moves = Graph()
for x in range(-BOARD_LENGTH, BOARD_LENGTH + 1):
    for y in range(-BOARD_HEIGHT, BOARD_HEIGHT + 1):
        if x == 0 or y == 0:
            rook.moves.add_new_node(x, y)
rook.moves.connect_adjacent_nodes()

queen = Unit()
queen.moves = QUEEN_TYPE
queen.name = "Queen"
queen.cost = 9
queen.moves = Graph()
for x in range(-BOARD_LENGTH, BOARD_LENGTH + 1):
    for y in range(-BOARD_HEIGHT, BOARD_HEIGHT + 1):
        if x == y or x == -y:
            queen.moves.add_new_node(x, y)
queen.moves.connect_diagonal_nodes()
for x in range(-BOARD_LENGTH, BOARD_LENGTH + 1):
    for y in range(-BOARD_HEIGHT, BOARD_HEIGHT + 1):
        if x == 0 or y == 0 and x != y:
            queen.moves.add_new_node(x, y)
queen.moves.connect_adjacent_nodes()

king = Unit()
king.moves = KING_TYPE
king.name = "King"
king.cost = 0
king.moves = Graph()
for x in range(-1, 2):
    for y in range (-1, 2):
        king.moves.add_new_node(x, y)
king.moves.connect_adjacent_nodes()
king.moves.connect_diagonal_nodes()

CARD_DICTIONARY = {
    WARPLING_TYPE: warpling,
    KNIGHT_TYPE: knight,
    BISHOP_TYPE: bishop,
    ROOK_TYPE: rook,
    QUEEN_TYPE: queen,
    KING_TYPE: king
}
