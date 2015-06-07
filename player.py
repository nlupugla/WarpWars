from constants import *

class Player:
    def __init__(self, color):
        self.color = color # WHITE or BLACK
        self.warp = 0
        self.palette = {WARPLING_TYPE: 'warpling', KNIGHT_TYPE: 'knight'}
