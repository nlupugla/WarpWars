from card import Card

class Player:
    """
    Players exist in the game and contain information about deploying units.

    A Player has a color, a number of warp, and a palette of cards from which they can deploy units.
    """
    def __init__(self, color, flipped=False):
        """
        Return a new player of the specified color.

        :param color: the color of the player, an int either WHITE or BLACK
        :param flipped: a boolean that when True, flips the movement of all the player's units
        :return:
        """
        self.color = color  # WHITE or BLACK
        self.warp = 1  # amount of warp available to the player
        self.palette = {}  # key: unit_type -> item: card
        self.flipped = flipped  # exactly one player should be flipped so all units move away from the starting zone

    def add_card(self, unit_type, amount):
        """
        Add a card to the player's palette.

        :param unit_type: an int corresponding to the unit type, eg: WARPLING_TYPE
        :param amount: the total number of units that can be deployed from the card
        :return: nothing
        """
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
            'palette': palette,
            'flipped': self.flipped
        }
        return dictionary
