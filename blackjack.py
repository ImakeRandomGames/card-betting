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



def draw_table(dealer_hand, player_hand):
    print "========================================"
    print "========================================"
    print "  Dealer has "
    for card in dealer_hand:
        print "    ", card
    print
    print " ~ ~ ~ ~ ~ ~ ~ ~ "
    print
    print "  Player has "
    for card in player_hand:
        print "    ", card
    print "========================================"
    print "========================================"

def respond(dealer, player, command):
    pass

def calculate_total(hand):
    pass


if __name__ == '__main__':
    deal_cards()