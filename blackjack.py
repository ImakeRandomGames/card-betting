from cards import Deck

deck = Deck()

dealer_hand = []
player_hand = []

game_mode = None

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

def deal_cards():

    dealer_card = deck.draw()
    dealer_card.facing = "down"
    dealer_hand.append(dealer_card)

    player_hand.append(deck.draw())
    dealer_hand.append(deck.draw())
    player_hand.append(deck.draw())


    if game_mode == "stdin":
        draw_table()
        while True:
            command = raw_input("What would you like to do? [s]tay, [h]it...")
            follow_command(command)

    else:
        return draw_table()


def draw_table(messages=None):

    if game_mode == "stdin":
        print "========================================"
        print "========================================"
        if any([card.facing == "down" for card in dealer_hand]):
            print "  Dealer has:"
        else:
            print "  Dealer has ({}):".format(sum_hand(dealer_hand))
        for card in dealer_hand:
            print "    ", card
        print
        print " ~ ~ ~ ~ ~ ~ ~ ~ "
        print
        print "  Player has ({}):".format(sum_hand(player_hand))
        for card in player_hand:
            print "    ", card
        print "========================================"
        print "========================================"

        if messages:
            print
            for message in messages:
                print "   {}    ".format(message.upper())
            print

    else:
        return {
            "player_hand": player_hand,
            "player_sum": sum_hand(player_hand),
            "dealer_hand": dealer_hand,
            "dealer_sum": sum_hand(dealer_hand),
        }


def sum_hand(hand):
    total = 0
    ace_count = 0
    for card in hand:
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

def follow_command(command):
    if command in ["hit", "h"]:
        player_hand.append(deck.draw())

        if sum_hand(player_hand) > 21:
            raise PlayerBusts()

        else:
            draw_table()

    if command in ["stay", "s"]:
        [card.show() for card in dealer_hand]

        while sum_hand(dealer_hand) < 17:
            dealer_hand.append(deck.draw())

        draw_table()
        if sum_hand(dealer_hand) > 21:
            raise DealerBusts()

        if sum_hand(player_hand) > sum_hand(dealer_hand):
            raise PlayerWins()

        if sum_hand(player_hand) < sum_hand(dealer_hand):
            raise DealerWins()

        if sum_hand(player_hand) == sum_hand(dealer_hand):
            raise Push()


if __name__ == '__main__':
    game_mode = "stdin"
    deal_cards()