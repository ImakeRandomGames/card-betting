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

    except PlayerWins as e:
        return "win"

    except DealerWins as e:
        return "lose"

    except Push as e:
        return "draw"

    return None

if __name__ == '__main__':

    stats = {
            "win": 0,
            "lose": 0,
            "draw": 0,
        }

    for _ in range(100):

        result = play()
        stats[result] += 1

    print stats