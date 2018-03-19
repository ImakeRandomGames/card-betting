# Card Betting

As I'm starting to learn a few schools of thought related to betting and card games, I figured it'd be worth building my own "automated casino" so that I could test different card game strategies and collect some of my own data.

The project layout is as follows:

 - `cards.py` has the base classes for cards and a deck
 - `blackjack.py` has the standard rules for dealing out hands, standard dealer logic and end game scenarios (via exceptions)
 - `player.py` contains all of the logic that a player would use to play the game

There are currently two (2) interfaces:

    python blackjack.py

This lets you play a single game via the command line, passing in `h` to hit or `s` to stay. The game will end with an exception that indicates the game's final state.

    python player.py [-n 1000]

This plays the specified number of games against the dealer, using the player logic in `player.py`, and prints out some summary statistics at the end.

Try tweaking the player logic to test your own strategies and see if you can win more than you lose!