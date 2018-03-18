import random

class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.facing = "up"

    def __repr__(self):
        if self.facing == "up":
            return "<Card: the {} of {}s>".format(self.rank, self.suit)
        else:
            return "<Card: the ???? of ????>"


class Deck(object):

    def __init__(self):
        self.cards = []
        for suit in ["spade", "club", "heart", "diamond"]:
            for rank in ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]:
                self.cards.append(Card(suit, rank))

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

