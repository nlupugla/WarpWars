"""
YOLO SWAG 420
"""

from flask import Flask, redirect, render_template, request

from game import Game

ROOT_TEMPLATE = 'root.html'
GAME_TEMPLATE = 'game.html'

app = Flask(__name__)

# master list of all currently running games
games = {}

@app.route('/')
def default_root():
    """
    Renders the root page.

    TODO: allow users to create/join games from here

    :return: the html for the root page
    """
    return render_template(ROOT_TEMPLATE)

@app.route('/create_game/<int:game_id>')
def create_game(game_id):
    """
    Create a new game with the given game_id.

    If the indicated game already exists a redirect to '/' will be returned.

    :param game_id: the game_id for the game to be created
    :return: a redirect to '/game/<game_id>' or '/'
    """
    # don't clobber existing games
    # TODO: make this more robust somehow
    if game_id in games: return redirect('/')

    games[game_id] = Game() # is this what the constructor takes?

    return redirect('/game/' + str(game_id))

@app.route('/game/<int:game_id>')
def game(game_id):
    """
    Renders the page for a given game.

    If the indicated game does not exist a redirect to '/' will be returned.

    :param game_id: the id of the game to display
    :return: the html page displaying the game or a redirect to '/'
    """
    # if there is no 'game_id' parameter, redirect
    if game_id == None: return redirect('/')

    return render_template(GAME_TEMPLATE, game_id = game_id)

if __name__ == '__main__':
    app.run()