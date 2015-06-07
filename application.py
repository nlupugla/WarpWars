"""
YOLO SWAG 420
"""

from flask import Flask, abort, redirect, render_template, request, url_for

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

@app.route('/create_game.html')
def create_game():
    """
    Create a new game.

    The id of the game to create must be given in the 'game_id' URL parameter.

    :return: nothing now; eventually the page for picking your King etc.
    """
    # get and format the game_id, redirecting if it doesn't exist
    gid = request.args.get('game_id')
    if gid == None: return redirect('/')
    game_id = int(gid)

    # don't clobber existing games
    # TODO: make this more robust somehow
    if game_id in games: return 'This game_id already taken'

    games[game_id] = Game() # is this what the constructor takes?


@app.route('/game.html')
def game():
    """
    Renders the page for a game.

    The id of the game must be given in the 'game_id' URL parameter.

    :return: the html for the game
    """
    game_id = request.args.get('game_id')

    # if there is no 'game_id' parameter, redirect
    if game_id == None: return redirect('/')

    return render_template(GAME_TEMPLATE, game_id = game_id)

if __name__ == '__main__':
    app.run()