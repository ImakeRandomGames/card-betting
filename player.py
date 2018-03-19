from blackjack import Game, PlayerWins, DealerWins, Push


class Strategy(object):
    def __init__(self):
        self.game = Game(mode="automated", print_games=False)
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


class AlwaysHitOnce(Strategy):

    def decide(self):
        if len(self.game.player_hand) == 2:
            return self.issue_command("hit")
        else:
            return self.issue_command("stay")


class SimpleSeventeen(Strategy):

    def decide(self):
        player_sum = self.game.sum_hand(self.game.player_hand)
        if player_sum < 17:
            return self.issue_command("hit")
        else:
            return self.issue_command("stay")


class SimpleDealerShowing(Strategy):

    def decide(self):
        player_sum = self.game.sum_hand(self.game.player_hand)
        if player_sum <= 11:  # can't bust
            return self.issue_command("hit")
        elif player_sum >= 17:  # close enough
            return self.issue_command("stay")
        else:
            dealer_sum = self.game.sum_hand(self.game.dealer_hand)
            if dealer_sum <= 6:  # hope dealer busts
                return self.issue_command("stay")
            else:  # have to chase them
                return self.issue_command("hit")


class Experimental(Strategy):

    def decide(self):
        player_sum = self.game.sum_hand(self.game.player_hand)
        if player_sum <= 11:
            return self.issue_command("hit")
        elif player_sum >= 18:
            return self.issue_command("stay")
        else:
            dealer_sum = self.game.sum_hand(self.game.dealer_hand)
            if dealer_sum <= 6:
                return self.issue_command("stay")
            else:
                return self.issue_command("hit")


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description="Let's automate some blackjack")
    parser.add_argument("-n", "--num", type=int, default=1000, help="How many rounds to you want to simulate")
    args = parser.parse_args()

    for strategy in [SimpleSeventeen, SimpleDealerShowing, Experimental]:

        stats = {
            "win": 0,
            "lose": 0,
            "draw": 0,
        }

        for _ in range(args.num):

            result = strategy().result
            stats[result] += 1

        win_pct = 100 * stats["win"] / float(args.num)
        loss_pct = 100 * stats["lose"] / float(args.num)

        print "{}:\t{}% win // {}% loss".format(strategy, win_pct, loss_pct)