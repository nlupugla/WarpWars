"""
YOLO SWAG 420
"""

from json import dumps

from flask import Flask, redirect, render_template, session, url_for

from constants import WHITE, BLACK
from game import Game, move
from tests import test_game

ROOT_TEMPLATE = 'root.html'
GAME_TEMPLATE = 'game.html'
ERROR_404_TEMPLATE = '404.html'

app = Flask(__name__)

# secret key for session storage
app.secret_key = 'THIS IS A TESTING KEY; CHANGE WHEN DEPLOYING, YOU NUMBSKULL'

# master list of all currently running games; list of their states
games = {}
game_states = {} # move this into Game eventually

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

    # set this player as white
    session['color-' + str(game_id)] = WHITE

    # actually create the game
    games[game_id] = test_game() #Game()
    game_states[game_id] = 0

    return redirect('/game/' + str(game_id))

@app.route('/join/game/<int:game_id>/as/<color>')
def join_game(game_id, color):
    """
    Join the given game as the player of the given color.

    If the indicated game does not exist or the color is not valid a redirect to '/' will be returned.

    :param game_id: the game_id of the game to join
    :param color: the color the player is joining as
    :return: a redirect to '/game/<game_id>' or '/'
    """
    # can only join games that actually exist
    if game_id not in games: return redirect(url_for('root'))

    # can only be white or black
    if color not in ('white', 'black'): return redirect(url_for('root'))

    # set the player's color as given
    session['color-' + str(game_id)] = WHITE if color == 'white' else BLACK

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

    drawing_file = url_for('static', filename = 'drawing.js')
    changed = url_for('game_changed', game_id = game_id, last_state = 0)[:-1] # remove the last_state so client can fill it in
    state = url_for('game_status', game_id = game_id)
    color = session['color-' + str(game_id)]
    return render_template(GAME_TEMPLATE, game_id = game_id, drawing_file = drawing_file, state = state,
                           changed = changed, player_color = color)

@app.route('/update/game/<int:game_id>/move/<int:unit_id>/to/<int:x>/<int:y>')
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
    if game_id not in games: return format_response('error', 'Game does not exist')
    # TODO: actually send the data to the backend and verify it before doing a legit state update
    # call Game.move
    games[game_id].move(unit_id, x, y)
    # TODO: game_states[game_id] += 1
    return format_response('success', 'default success!') # game_status(game_id)

@app.route('/changed/game/<int:game_id>/<int:last_state>')
def game_changed(game_id, last_state):
    """
    Indicate to the client whether or not it needs to refetch game state.

    :param game_id: the game_id of the game to be checked for new state
    :param last_state: the last state seen by the client
    :return: whether or not there is new state to be fetched or an error, as JSON
    """
    if game_id not in games: return format_response('error', 'Game does not exist')
    return dumps({'changed': True if game_states[game_id] > last_state else False}) # absolutely disgusting

@app.route('/state/game/<int:game_id>')
def game_status(game_id):
    """
    Fetch the full game state of a given game.

    If a game with the given game_id does not exist an error will be returned instead.

    :param game_id: the id of the game whose status is to be fetched
    :return: the current game state or an error, as JSON
    """
    if game_id not in games: return format_response('error', 'Game does not exist')
    return games[game_id].state()

@app.errorhandler(404)
def page_not_found(error):
    """
    Return a friendly 404 page.

    :param error: the error message
    :return: a friendly 404 page
    """
    return render_template(ERROR_404_TEMPLATE)

def format_response(status, message):
    """
    Format a status and message as a JSON object suitable for returning to the browser.

    :param status: the status of the message (eg 'error', 'success')
    :param message: the message to format
    :return: a JSON object containing the error message
    """
    return dumps({'status': status, 'message': message})

if __name__ == '__main__':
    app.run()