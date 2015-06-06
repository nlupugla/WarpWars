"""
YOLO SWAG 420
"""

from flask import Flask, abort, redirect, render_template, url_for

ROOT_TEMPLATE = 'root.html'

app = Flask(__name__)

"""
Render the root page
Stub for now
TODO: allow users to create/join games from here
"""
@app.route('/')
def default_root():
    return render_template(ROOT_TEMPLATE)