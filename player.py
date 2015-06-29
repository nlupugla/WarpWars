from card import Card

class Player:
    """
    Players exist in the game and contain information about deploying units.

    A Player has a color, a number of warp, and a palette of cards from which they can deploy units.
    """
    def __init__(self, color):
        self.color = color  # WHITE or BLACK
        self.warp = 1  # amount of warp available to the player
        self.palette = {}  # key: unit_type -> item: card

    def add_card(self, unit_type, amount):
        self.palette[unit_type] = Card(unit_type, amount)

    def generate_dict(self):
        """
        Create a dictionary object containing all of the player's data to be sent to the client.

        :return: a dictionary formatted to be an argument for json.dumps
        """
        palette = []
        for unit_type in self.palette:
            palette.append(self.palette[unit_type].generate_dict())
        dictionary = {
            'color': self.color,
            'warp': self.warp,
            'palette': palette
        }
        return dictionary
