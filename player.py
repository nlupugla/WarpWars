class Player:
    def __init__(self, color):
        self.color = color  # WHITE or BLACK
        self.warp = 0
        self.palette = {}  # key: unit_type -> item: card

    def generate_dict(self):
        palette = []
        for unit_type in self.palette:
            palette.append(self.palette[unit_type].generate_dict())
        dictionary = {
            'color': self.color,
            'warp': self.warp,
            'palette': palette
        }
        return dictionary
