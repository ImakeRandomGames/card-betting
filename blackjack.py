from cards import Deck

#
# Game End States
#

class GameOver(Exception):
    pass  # base

class Push(GameOver):
    pass

class PlayerWins(GameOver):
    pass

class DealerWins(GameOver):
    pass

class DealerBusts(PlayerWins):
    pass

class PlayerBusts(DealerWins):
    pass


class Game(object):

    def __init__(self, mode=None):

        self.deck = Deck()
        self.mode = mode

        self.dealer_hand = []
        self.player_hand = []

        # deal out initial cards
        dealer_card = self.deck.draw()
        dealer_card.facing = "down"

        self.dealer_hand.append(dealer_card)
        self.player_hand.append(self.deck.draw())
        self.dealer_hand.append(self.deck.draw())
        self.player_hand.append(self.deck.draw())

        if self.mode == "stdin":
            while True:
                print self
                command = raw_input("What would you like to do? [s]tay, [h]it...")
                self.dealer_command(command)


    def __repr__(self):
        stdout = "========= A GAME OF BLACKJACK ==========\n"
        if any([card.facing == "down" for card in self.dealer_hand]):
            stdout += "  Dealer has:\n"
        else:
            stdout += "  Dealer has ({}):\n".format(self.sum_hand(self.dealer_hand))
        for card in self.dealer_hand:
            stdout += "    {}\n".format(card)

        stdout += " ~ ~ ~ ~ ~ ~ ~ ~ \n"

        stdout += "  Player has ({}):\n".format(self.sum_hand(self.player_hand))
        for card in self.player_hand:
            stdout += "    {}\n".format(card)
        stdout += "========================================\n"

        return stdout


    @staticmethod
    def sum_hand(hand):
        total = 0
        ace_count = 0
        for card in hand:
            if card.facing == "down":
                continue

            try:
                total += int(card.rank)
            except:
                if card.rank in ["jack", "queen", "king"]:
                    total += 10
                elif card.rank == "ace":
                    ace_count += 1

        # assume aces are 11 unless you'd bust, then 1
        for x in range(ace_count):
            if total <= 10:
                total += 11
            else:
                total += 1

        return total


    def dealer_command(self, command):

        if command in ["hit", "h"]:
            print " => player has chosen to hit"

            self.player_hand.append(self.deck.draw())

            print self

            if self.sum_hand(self.player_hand) > 21:
                raise PlayerBusts()


        if command in ["stay", "s"]:
            print " => player has chosen to stay"

            [card.show() for card in self.dealer_hand]

            while self.sum_hand(self.dealer_hand) < 17:
                self.dealer_hand.append(self.deck.draw())

            print self

            if self.sum_hand(self.dealer_hand) > 21:
                raise DealerBusts()

            if self.sum_hand(self.player_hand) > self.sum_hand(self.dealer_hand):
                raise PlayerWins()

            if self.sum_hand(self.player_hand) < self.sum_hand(self.dealer_hand):
                raise DealerWins()

            if self.sum_hand(self.player_hand) == self.sum_hand(self.dealer_hand):
                raise Push()


if __name__ == '__main__':
    Game(mode="stdin")