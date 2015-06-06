"""
YOLO SWAG 420
"""

from flask import Flask, abort, redirect, render_template, url_for

ROOT_TEMPLATE = 'root.html'

app = Flask(__name__)

@app.route('/')
def default_root():
    """
    Renders the root page.
    TODO: allow users to create/join games from here
    :return: the html for the root page
    """
    return render_template(ROOT_TEMPLATE)

if __name__ == '__main__':
    app.run()