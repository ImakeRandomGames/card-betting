from blackjack import deal_cards, follow_command, draw_table, PlayerWins, DealerWins, Push


def play():

    game = deal_cards()
    game_result = None

    while True:


        print draw_table()

        if game["player_sum"] <= 11:
            game_result = issue_command("hit")
        elif game["player_sum"] >= 17:
            game_result = issue_command("stay")

        else:
            for card in game["dealer_hand"]:
                if card.facing == "up":  # no peeking!
                    if card.rank <= 6:
                        game_result = issue_command("stay")
                    else:
                        game_result = issue_command("hit")

        if game_result:
            break

    return game_result

def issue_command(cmd):
    print "decided to", cmd

    try:

        follow_command(cmd)
        return None

    except PlayerWins as e:
        return "win"

    except DealerWins as e:
        return "lose"

    except Push as e:
        return "draw"

    return None

if __name__ == '__main__':

    for _ in range(100):

        stats = {
            "win": 0,
            "lose": 0,
            "draw": 0,
        }

        result = play()
        stats[result] += 1

    print stats