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
warpling.moves.add_new_node(0, 1)
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
queen.type = QUEEN_TYPE
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
king.type = KING_TYPE
king.name = "King"
king.cost = 0
king.moves = Graph()
for x in range(-1, 2):
    for y in range(-1, 2):
        king.moves.add_new_node(x, y)
king.moves.connect_adjacent_nodes()
king.moves.connect_diagonal_nodes()

gold_general = Unit()
gold_general.type = GOLD_GENERAL_TYPE
gold_general.name = "Gold General"
gold_general.cost = 4
gold_general.moves = Graph()
for x in range(-1, 1):
    for y in range(0, 1):
        gold_general.moves.add_new_node(x, y)
gold_general.moves.add_new_node(0, -1)
gold_general.moves.connect_adjacent_nodes()

silver_general = Unit()
silver_general.type = SILVER_GENERAL_TYPE
silver_general.name = "Silver General"
silver_general.cost = 2
silver_general.moves = Graph()
for x in range(-1, 1):
    silver_general.moves.add_new_node(x, 1)
silver_general.moves.add_new_node(0, 0)
silver_general.moves.add_new_node(-1, -1)
silver_general.moves.add_new_node(1, -1)
silver_general.moves.connect_all_to(silver_general.moves.find_node_by_position(0, 0))

lance = Unit()
lance.type = LANCE_TYPE
lance.name = "Lance"
lance.cost = 2
lance.moves = Graph()
for y in range(0, BOARD_HEIGHT + 1):
    lance.moves.add_new_node(0, y)
lance.moves.connect_adjacent_nodes()

pawn = Unit()
pawn.type = PAWN_TYPE
pawn.name = "Pawn"
pawn.cost = 0
pawn.moves = Graph()
for y in range(0, 1):
    pawn.moves.add_new_node(0, y)
pawn.moves.connect_adjacent_nodes()

promoted_rook = Unit()
promoted_rook.type = PROMOTED_ROOK_TYPE
promoted_rook.name = "Promoted Rook"
promoted_rook.cost = 7
promoted_rook.moves = Graph()
for x in range(-1, 1):
    for y in range(-1, 1):
        if x == y or x == -y:
            promoted_rook.moves.add_new_node(x, y)
promoted_rook.moves.connect_diagonal_nodes()
for x in range(-BOARD_LENGTH, BOARD_LENGTH + 1):
    for y in range(-BOARD_HEIGHT, BOARD_HEIGHT + 1):
        if x == 0 or y == 0 and x != y:
            promoted_rook.moves.add_new_node(x, y)
promoted_rook.moves.connect_adjacent_nodes()

promoted_bishop = Unit()
promoted_bishop.type = PROMOTED_BISHOP_TYPE
promoted_bishop.name = "Promoted Bishop"
promoted_bishop.cost = 6
promoted_bishop.moves = Graph()
for x in range(-BOARD_LENGTH, BOARD_LENGTH + 1):
    for y in range(-BOARD_HEIGHT, BOARD_HEIGHT + 1):
        if x == y or x == -y:
            promoted_bishop.moves.add_new_node(x, y)
promoted_bishop.moves.connect_diagonal_nodes()
for x in range(-1, 1):
    for y in range(-1, 1):
        if x == 0 or y == 0 and x != y:
            promoted_bishop.moves.add_new_node(x, y)
promoted_bishop.moves.connect_adjacent_nodes()

CARD_DICTIONARY = {
    WARPLING_TYPE: warpling,
    KNIGHT_TYPE: knight,
    BISHOP_TYPE: bishop,
    ROOK_TYPE: rook,
    QUEEN_TYPE: queen,
    KING_TYPE: king,
    GOLD_GENERAL_TYPE: gold_general,
    SILVER_GENERAL_TYPE: silver_general,
    LANCE_TYPE: lance,
    PAWN_TYPE: pawn,
    PROMOTED_ROOK_TYPE: promoted_rook,
    PROMOTED_BISHOP_TYPE: promoted_bishop
}
