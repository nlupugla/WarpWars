from card_dictionary import CARD_DICTIONARY

class Card:

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
            'current_amount': self.current_amount,  # TODO: change
            'starting_amount': self.starting_amount
        }
        return dictionary
