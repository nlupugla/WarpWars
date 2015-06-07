from constants import *

class Player:
    def __init__(self, color):
        self.color = color # WHITE or BLACK
        self.warp = 0
        self.palette = {0: 'warpling', 1: 'knight'}
