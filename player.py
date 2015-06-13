from constants import *

class Player:
    def __init__(self, color):
        self.color = color # WHITE or BLACK
        self.warp = 0
        self.palette = {WARPLING_TYPE: 1, KNIGHT_TYPE: 1} # temporary: for testing purposes
