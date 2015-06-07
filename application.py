"""
YOLO SWAG 420
"""

from json import dumps

from flask import Flask, redirect, render_template

from game import Game

ROOT_TEMPLATE = 'root.html'
GAME_TEMPLATE = 'game.html'

app = Flask(__name__)

# master list of all currently running games
games = {}

@app.route('/')
def render_root():
    """
    Render the root page.

    TODO: allow users to create/join games from here

    :return: the html for the root page
    """
    return render_template(ROOT_TEMPLATE)

@app.route('/create/game/<int:game_id>')
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
    Render the page for a given game.

    If the indicated game does not exist a redirect to '/' will be returned.

    :param game_id: the id of the game to display
    :return: the html page displaying the game or a redirect to '/'
    """
    # if there is no 'game_id' parameter, redirect
    if game_id == None: return redirect('/')

    return render_template(GAME_TEMPLATE, game_id = game_id)

@app.route('/update/game/<int:game_id>/move/<int:unit_id>/to/<int:x>/<int:y>')
def game_update_move(game_id, unit_id, x, y):
    """
    Move a given unit in the given game to the given position.

    The backend checks whether the move is valid and then returns the new game state. This state, or an error message if the move was illegal, is then returned.

    :param game_id: the game containing the unit that is moving
    :param unit_id: the id of the unit that is moving
    :param x: the x-coordinate the piece is moving to
    :param y: the y-coordinate the piece is moving to
    :return: the game state after the move, as JSON
    """
    return format_error('default success!')

def format_error(error_message):
    """
    Format an error message as a JSON object suitable for returning to the browser.

    :param error_message: the error message to format
    :return: a JSON object containing the error message
    """
    return dumps({'status': 'error', 'message': error_message})

if __name__ == '__main__':
    app.run()