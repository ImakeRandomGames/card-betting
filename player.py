from blackjack import Game, PlayerWins, DealerWins, Push


def play():

    game = Game()

    while True:

        player_sum = game.sum_hand(game.player_hand)


        if player_sum <= 11:
            game_result = issue_command(game, "hit")
        elif player_sum >= 17:
            game_result = issue_command(game, "stay")

        else:
            dealer_sum = game.sum_hand(game.dealer_hand)

            if dealer_sum <= 6:
                game_result = issue_command(game, "stay")
            else:
                game_result = issue_command(game, "hit")

        if game_result:
            break

    return game_result

def issue_command(game, cmd):
    try:

        game.dealer_command(cmd)
        return None

    except PlayerWins:
        return "win"

    except DealerWins:
        return "lose"

    except Push:
        return "draw"

    return None

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description="Let's automate some blackjack")
    parser.add_argument("-n", "--num", type=int, default=1000, help="How many rounds to you want to simulate")
    args = parser.parse_args()

    stats = {
            "win": 0,
            "lose": 0,
            "draw": 0,
        }

    for _ in range(args.num):

        result = play()
        stats[result] += 1

    print stats