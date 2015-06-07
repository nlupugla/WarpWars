"""
YOLO SWAG 420
"""

from json import dumps

from flask import Flask, redirect, render_template, url_for

from game import Game

ROOT_TEMPLATE = 'root.html'
GAME_TEMPLATE = 'game.html'
ERROR_404_TEMPLATE = '404.html'

app = Flask(__name__)

# master list of all currently running games
games = {}

@app.route('/')
def root():
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
    if game_id in games: return redirect(url_for('root'))

    games[game_id] = Game()

    return redirect('/game/' + str(game_id))

@app.route('/game/<int:game_id>')
def game(game_id):
    """
    Render the page for a given game.

    If the indicated game does not exist a redirect to '/' will be returned.

    :param game_id: the id of the game to display
    :return: the html page displaying the game or a redirect to '/'
    """
    # if the given game doesn't exist, redirect to '/'
    if game_id not in games: return redirect(url_for('root'))

    return render_template(GAME_TEMPLATE, game_id = game_id, drawing_file = url_for('static', filename = 'drawing.js'))

@app.route('/update/game/<int:game_id>/move/<int:unit_id>/to/<int:x>/<int:y>', methods = ['POST'])
def game_update_move(game_id, unit_id, x, y):
    """
    Move a given unit in the given game to the given position.

    The backend checks whether the move is valid and then returns the new game state. This state, or an error message if the move was illegal, is then returned.

    An error will also be returned if the indicated game does not exist.

    :param game_id: the game containing the unit that is moving
    :param unit_id: the id of the unit that is moving
    :param x: the x-coordinate the piece is moving to
    :param y: the y-coordinate the piece is moving to
    :return: the game state after the move, as JSON
    """
    if game_id not in games: return format_error('Game does not exist')
    # TODO: actually send the data to the backend and verify it before returning a legit state update
    return format_error('default success!') # game_status(game_id)

@app.route('/state/game/<int:game_id>')
def game_status(game_id):
    """
    Fetch the full game state of a given game.

    If a game with the given game_id does not exist an error will be returned instead.

    :param game_id: the id of the game whose status is to be fetched
    :return: the current game state or an error, as JSON
    """
    if game_id not in games: return format_error('Game does not exist')
    return games[game_id].state()

@app.errorhandler(404)
def page_not_found(error):
    """
    Return a friendly 404 page.

    :param error: the error message
    :return: a friendly 404 page
    """
    return render_template(ERROR_404_TEMPLATE)

def format_error(error_message):
    """
    Format an error message as a JSON object suitable for returning to the browser.

    :param error_message: the error message to format
    :return: a JSON object containing the error message
    """
    return dumps({'status': 'error', 'message': error_message})

if __name__ == '__main__':
    app.run()