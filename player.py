import random

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

    def issue_command(self, cmd, game=None):
        try:
            if game:
                game.dealer_command(cmd)
            else:
                self.game.dealer_command(cmd)
            return None

        except PlayerWins:
            return "win"

        except DealerWins:
            return "lose"

        except Push:
            return "draw"

        return None


class Random(Strategy):
    def decide(self):
        return self.issue_command(random.choice(["hit", "stay"]))


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

class MonteCarlo(Strategy):
    """
    Play the exact same game out randomly a bunch of times
    and see which move empirically leads to the best outcome,
    then do that.
    """

    def debug(self, msg):
        if False:
            print msg

    def info(self, msg):
        if False:
            print msg

    def decide(self):
        moves = ["hit", "stay"]
        results_by_first_move = {
            "hit": {
                "games": 0,
                "wins": 0,
            },
            "stay": {
                "games": 0,
                "wins": 0,
            }
        }
        for _ in range(500):

            # clone the current game, using list() so we don't pass references
            simulated_game = Game(mode="automated")
            simulated_game.dealer_hand = list(self.game.dealer_hand)
            simulated_game.player_hand = list(self.game.player_hand)

            self.debug(simulated_game)

            # make a first move, see if the game ends
            first_move = random.choice(moves)
            self.debug("- first move {}".format(first_move))
            game_result = self.issue_command(first_move, game=simulated_game)
            if game_result:
                results_by_first_move[first_move]["games"] += 1
                if game_result == "win":
                    self.debug(" - won on first move")
                    results_by_first_move[first_move]["wins"] += 1
                else:
                    self.debug(" - lost on first move")

            else: # continue playing the game randomly and see what happens

                while True:
                    game_result = self.issue_command(random.choice(moves), game=simulated_game)
                    if game_result:
                        break

                results_by_first_move[first_move]["games"] += 1
                if game_result == "win":
                    self.debug(" - won on subsequent move")
                    results_by_first_move[first_move]["wins"] += 1
                else:
                    self.debug(" - lost on subsequent move")

            # print simulated_game

        self.info("=============")
        self.info(results_by_first_move)

        # calculate the win pct for both first moves
        hit_win_pct = results_by_first_move["hit"]["wins"] / float(results_by_first_move["hit"]["games"])
        stay_win_pct = results_by_first_move["stay"]["wins"] / float(results_by_first_move["stay"]["games"])

        # issue the winning command
        if hit_win_pct > stay_win_pct:
            self.info("=> choosing to 'hit' with a {}% win rate".format(hit_win_pct*100))
            return self.issue_command("hit")
        else:
            self.info("=> choosing to 'stay' with a {}% win rate".format(stay_win_pct*100))
            return self.issue_command("stay")



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
    parser.add_argument("-n", "--num", type=int, default=10000, help="How many rounds to you want to simulate")
    parser.add_argument("-r", "--random", action="store_true", help="Do you want to test the 'random' strategies?")
    parser.add_argument("-s", "--simple", action="store_true", help="Do you want to test the 'simple' strategies?")
    parser.add_argument("-m", "--monte", action="store_true", help="Do you want to test the 'monte carlo' strategy?")
    args = parser.parse_args()

    strategies = []
    if args.random:
        strategies.extend([Random, AlwaysHitOnce])
    if args.simple:
        strategies.extend([SimpleSeventeen, SimpleDealerShowing])
    if args.monte:
        strategies.extend([MonteCarlo])

    for strategy in strategies:

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