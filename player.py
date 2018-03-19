from blackjack import Game, PlayerWins, DealerWins, Push


class Strategy(object):
    def __init__(self):
        self.game = Game()
        self.result = self.play()

    def play(self):
        while True:
            game_result = self.decide()

            if game_result:
                break

        return game_result


    def decide(self):
        raise NotImplementedError

    def issue_command(self, cmd):
        try:

            self.game.dealer_command(cmd)
            return None

        except PlayerWins:
            return "win"

        except DealerWins:
            return "lose"

        except Push:
            return "draw"

        return None


class SimpleSeventeen(Strategy):

    def decide(self):
        player_sum = self.game.sum_hand(self.game.player_hand)
        if player_sum < 17:
            game_result = self.issue_command("hit")
        elif player_sum >= 17:
            game_result = self.issue_command("stay")

        return game_result

class SimpleDealerShowing(Strategy):



    def decide(self):
        player_sum = self.game.sum_hand(self.game.player_hand)
        if player_sum <= 11:  # can't bust
            game_result = self.issue_command("hit")
        elif player_sum >= 17:  # close enough
            game_result = self.issue_command("stay")
        else:
            dealer_sum = self.game.sum_hand(self.game.dealer_hand)
            if dealer_sum <= 6:  # hope dealer busts
                game_result = self.issue_command("stay")
            else:  # have to chase them
                game_result = self.issue_command("hit")

        return game_result



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

        result = SimpleSeventeen().result
        stats[result] += 1

    print stats