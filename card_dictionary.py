import unit
from constants import *
from move import *
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
knight.type = KNIGHT_TYPE

warpling = unit.Unit()
warpling.moves = [
    [Move(NORTH)],
    [Move(EAST)],
    [Move(SOUTH)],
    [Move(WEST)]
]
warpling.type = WARPLING_TYPE

CARD_DICTIONARY = {
    'knight': knight,
    'warpling': warpling
}