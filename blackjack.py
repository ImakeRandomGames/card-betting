from cards import Deck

def deal_cards():
    deck = Deck()

    dealer_hand = []
    player_hand = []

    dealer_card = deck.draw()
    dealer_card.facing = "down"
    dealer_hand.append(dealer_card)

    player_hand.append(deck.draw())
    dealer_hand.append(deck.draw())
    player_hand.append(deck.draw())

    draw_table(dealer_hand, player_hand)

    while True:
        command = raw_input("What would you like to do? [s]tay, [h]it...")

        if command in ["hit", "h"]:
            player_hand.append(deck.draw())

            if sum_hand(player_hand) > 21:
                return draw_table(dealer_hand, player_hand, ["you busted"])

            else:
                draw_table(dealer_hand, player_hand)
                continue

        if command in ["stay", "s"]:
            [card.show() for card in dealer_hand]

            while sum_hand(dealer_hand) < 17:
                dealer_hand.append(deck.draw())

            if sum_hand(dealer_hand) > 21:
                return draw_table(dealer_hand, player_hand, ["dealer busted", "you win"])

            if sum_hand(player_hand) > sum_hand(dealer_hand):
                return draw_table(dealer_hand, player_hand, ["dealer stays", "you win"])

            if sum_hand(player_hand) < sum_hand(dealer_hand):
                return draw_table(dealer_hand, player_hand, ["dealer stays", "you lose"])

            if sum_hand(player_hand) == sum_hand(dealer_hand):
                return draw_table(dealer_hand, player_hand, ["dealer stays", "push"])


def draw_table(dealer_hand, player_hand, messages=None):
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


if __name__ == '__main__':
    deal_cards()