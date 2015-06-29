from card_dictionary import CARD_DICTIONARY

class Card:
    """
    Cards live in player palettes and help determine which units the player can deploy.

    Each card is closely associated with a unit type, so has the name, type, and cost of that unit. In addition, a Card
    has a certain starting_amount, which is the total number of units of said type the player can deploy, and a
    current_amount, which decreases as the player deploys and is the number the player currently has left to deploy.
    """

    def __init__(self, unit_type, amount):
        unit = CARD_DICTIONARY[unit_type]
        self.name = unit.name
        self.type = unit_type
        self.cost = unit.cost
        self.current_amount = amount
        self.starting_amount = amount

    def generate_dict(self):
        dictionary = {
            'name': self.name,
            'type': self.type,
            'cost': self.cost,
            'current_amount': self.current_amount,
            'starting_amount': self.starting_amount
        }
        return dictionary
