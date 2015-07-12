"""
YOLO SWAG 420
"""

from json import dumps

from flask import Flask, redirect, render_template, session, url_for

from constants import WHITE, BLACK
from game import Game
from tests import test_game, make_game

ROOT_TEMPLATE = 'root.html'
GAME_TEMPLATE = 'game.html'
ERROR_404_TEMPLATE = '404.html'

STATUS_SUCCESS = 'success'
STATUS_ERROR = 'error'

ERROR_GAME_DNE = 'game does not exist'
ERROR_MASQUERADE = 'cannot perform actions as opponent'
SUCCESS_DEFAULT = 'success'

DEBUG_SECRET_KEY = 'THIS IS A TESTING KEY; CHANGE WHEN DEPLOYING, YOU NUMBSKULL'

DEBUG = True # change this when deploying, obviously

app = Flask(__name__)

# secret key for session storage
app.secret_key = DEBUG_SECRET_KEY

# master list of all currently running games; list of their states
games = {}

@app.route('/')
def root():
    """
    Render the root page.

    TODO: allow users to create games from here

    :return: the html for the root page
    """
    num_games = len(games)
    list_of_games = games.keys()
    return render_template(ROOT_TEMPLATE, num_games = num_games, games = list_of_games)

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

    # set this player as black
    session['color-' + str(game_id)] = BLACK

    # actually create the game
    games[game_id] = make_game() #test_game()

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

    drawing_file = generate_static_url('drawing.js')
    changed = url_for('game_changed', game_id = game_id, last_state = 0)[:-1] # remove last_state so client can fill it in
    state = url_for('game_status', game_id = game_id)
    end_turn = url_for('game_update_end_turn', game_id = game_id)
    color = session['color-' + str(game_id)]
    return render_template(GAME_TEMPLATE, game_id = game_id, drawing_file = drawing_file, state = state,
                           changed = changed, end_turn = end_turn, player_color = color)

@app.route('/update/game/<int:game_id>/move/<int:unit_id>/to/<int:x>/<int:y>')
def game_update_move(game_id, unit_id, x, y):
    """
    Move a given unit in the given game to the given position.

    The backend checks whether the move is valid and then updates the game state. This state, or an error message if the move was illegal, is then returned.

    An error will also be returned if the indicated game does not exist.

    :param game_id: the id of the game containing the unit to be moved
    :param unit_id: the id of the unit that is moving
    :param x: the x-coordinate the piece is moving to
    :param y: the y-coordinate the piece is moving to
    :return: whether or not the update succeeded, as JSON
    """
    if game_id not in games: return format_response(STATUS_ERROR, ERROR_GAME_DNE)
    games[game_id].move(unit_id, x, y)
    return format_response(STATUS_SUCCESS, SUCCESS_DEFAULT) # maybe return game_status(game_id), or just wait for autoupdate?

@app.route('/update/game/<int:game_id>/color/<int:color>/deploy/<int:unit_type>/to/<int:x>/<int:y>')
def game_update_deploy(game_id, color, unit_type, x, y):
    """
    Deploy a unit of the given type to the given position.

    The backend checks whether the deployment is valid and then updates the game state. This state, or an error message if the deployment was illegal, is then returned.

    An error will also be returned if the indicated game does not exist or the player ordered a deployment for their opponent.

    :param game_id: the id of the game containing the unit to be moved
    :param color: the color of the player deploying the unit ie the of the unit to be deployed
    :param unit_type: the type of the unit to be deployed
    :param x: the x-coordinate to deploy the unit to
    :param y: the y-coordinate to deploy the unit to
    :return: whether or not the deployment succeeded, as JSON
    """
    if game_id not in games: return format_response(STATUS_ERROR, ERROR_GAME_DNE)
    if color != session['color-' + str(game_id)]: return format_response(STATUS_ERROR, ERROR_MASQUERADE)
    games[game_id].deploy(unit_type, color, x, y)
    return format_response(STATUS_SUCCESS, SUCCESS_DEFAULT)

@app.route('/update/game/<int:game_id>/end/turn')
def game_update_end_turn(game_id):
    """
    End the current turn of the given game.

    :param game_id: the id of the game to update
    :return: whether or not the update succeeded, as JSON
    """
    if game_id not in games: return format_response(STATUS_ERROR, ERROR_GAME_DNE)
    games[game_id].next_turn()
    return format_response(STATUS_SUCCESS, SUCCESS_DEFAULT)

@app.route('/changed/game/<int:game_id>/<int:last_state>')
def game_changed(game_id, last_state):
    """
    Indicate to the client whether or not it needs to refetch game state.

    :param game_id: the game_id of the game to be checked for new state
    :param last_state: the last state seen by the client
    :return: whether or not there is new state to be fetched or an error, as JSON
    """
    if game_id not in games: return format_response(STATUS_ERROR, ERROR_GAME_DNE)
    return dumps({'changed': True if games[game_id].state_ID > last_state else False}) # absolutely disgusting

@app.route('/state/game/<int:game_id>')
def game_status(game_id):
    """
    Fetch the full game state of a given game.

    If a game with the given game_id does not exist an error will be returned instead.

    :param game_id: the id of the game whose status is to be fetched
    :return: the current game state or an error, as JSON
    """
    if game_id not in games: return format_response(STATUS_ERROR, ERROR_GAME_DNE)
    return games[game_id].state()

@app.errorhandler(404)
def page_not_found(error):
    """
    Return a friendly 404 page.

    :param error: the error message
    :return: a friendly 404 page
    """
    return render_template(ERROR_404_TEMPLATE)

# utility functions

def format_response(status, message):
    """
    Format a status and message as a JSON object suitable for returning to the browser.

    :param status: the status of the message (eg 'error', 'success')
    :param message: the message to format
    :return: a JSON object containing the error message
    """
    return dumps({'status': status, 'message': message})

def generate_static_url(file_name):
    """
    Generate URLs for static files according to the relevant static file root.

    :param file_name: the name or path of the file to generate a path to
    :return: a properly formatted URL to the given file
    """
    if DEBUG:
        return url_for('static', filename = file_name)
    else:
        return '/%s' % file_name # the front-end proxy will handle it for us

# TODO: also send the color of the unit to be deployed/moved in the URL and check that against the player in the cookie
# TODO: and the active player/unit color on the backend
# TODO: to prevent move spoofing; this also for deploy and end turn

if __name__ == '__main__':
    if not DEBUG and app.secret_key == DEBUG_SECRET_KEY:
        print 'ERROR: default secret key cannot be used in production!'
        print 'Exiting!'
        raise SystemExit
    app.run(debug = DEBUG)