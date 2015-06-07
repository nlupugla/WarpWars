from game import *
from unit import *
from player import *
from card_dictionary import *

def test_game():
    return_game = Game()
    return_game.active_color = WHITE
    return_game.place(CARD_DICTIONARY['warpling'], 5, 5)
    return_game.active_color = BLACK
    return_game.place(CARD_DICTIONARY['warpling'], 6, 6)
    return return_game

if __name__ == '__main__':
    game = Game()
    player1 = Player(WHITE)
    player2 = Player(BLACK)
    game.players = [player1, player2]
    game.active_color = WHITE
    game.place(CARD_DICTIONARY['knight'], 5, 5)
    game.active_color = BLACK
    game.place(CARD_DICTIONARY['warpling'], 6, 6)

    print game.board[5][5] == WHITE_TILE
    print game.board[6][6] == BLACK_TILE
