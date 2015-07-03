# WarpWars
An online turn-based strategy game.

Written in Python with [Flask](https://github.com/mitsuhiko/flask).

As a Flask app, WarpWars can be run in the usual way with [Gunicorn](http://gunicorn.org), but will break if more than 1 worker thread is used, due to state dependencies.