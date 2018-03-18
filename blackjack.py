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
            draw_table(dealer_hand, player_hand)

            if calculate_total(player_hand) > 21:
                print
                print "    YOU BUSTED    "
                print
                return

            else:
                continue

        if command in ["stay", "s"]:
            [card.show() for card in dealer_hand]

            while calculate_total(dealer_hand) < 17:
                dealer_hand.append(deck.draw())

            draw_table(dealer_hand, player_hand)

            if calculate_total(dealer_hand) > 21:
                print
                print "    DEALER BUSTED    "
                print "    YOU WIN !!!!!    "
                print
                return

            if calculate_total(player_hand) > calculate_total(dealer_hand):
                print
                print "    YOU WIN !!!!!    "
                print
                return

            if calculate_total(player_hand) < calculate_total(dealer_hand):
                print
                print "    YOU LOSE    "
                print
                return

            if calculate_total(player_hand) == calculate_total(dealer_hand):
                print
                print "    PUSH    "
                print
                return


def draw_table(dealer_hand, player_hand):
    print "========================================"
    print "========================================"
    print "  Dealer has:"
    for card in dealer_hand:
        print "    ", card
    print
    print " ~ ~ ~ ~ ~ ~ ~ ~ "
    print
    print "  Player has ({}):".format(calculate_total(player_hand))
    for card in player_hand:
        print "    ", card
    print "========================================"
    print "========================================"


def calculate_total(hand):
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