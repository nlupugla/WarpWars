from game import *
from unit import *
from player import *
from card_dictionary import *

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

if __name__ == '__main__':
    game = test_game()

    # test that things were set up properly
    print game.board[5][5] == WHITE_TILE
    print game.board[6][6] == BLACK_TILE
    print game.units
    print game.units[1].x == 5
    print game.units[2].x == 6

    # test that moving works as it should
    print not game.move(1, 6, 6) # should print true as this is out of range
    print game.board[6][6] == BLACK_TILE # should still be true
    game.move(1, 5, 6)
    print game.board[5][6] == WHITE_TILE
    game.move(1, 6, 6)
    print game.board[6][6] == WHITE_TILE
    del game.units[2]
    print game.units


    print game.state()
