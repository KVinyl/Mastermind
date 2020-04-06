from collections import Counter, namedtuple
from random import randint


Feedback = namedtuple('Feedback', ['blacks', 'whites'])


class Mastermind():
    def __init__(self, pegs=4, colors=6, turns=12):
        """Parameters: pegs, colors, and turns must be postive integers

        The generated code to be decoded by the player is represented as a
        tuple of integers with the length of pegs. Each integer in the tuple
        is a randomized integer from 1 to colors inclusively.

        The value of the integer represents a type of color.
        """
        self.pegs = pegs
        self.colors = colors
        self.turns = turns

        self.code = tuple(randint(1, self.colors) for _ in range(self.pegs))
        self.guesses = {}
        self.fbs = {}
        self.won = False

    def victory(self):
        """Return whether the game was won."""
        return self.won

    def game_over(self):
        """Return whether the game is over."""
        return self.victory() or len(self.guesses) == self.turns

    def guess(self, guessed_code):
        """Parameter, guessed_code, is a tuple of integers.

        if and only if len(guessed_code) == pegs, then feedback will be
        evaluated and stored.

        The guessed code and the feedback of the guessed code are added
        to correspond with the turn number.
        """
        if not self.game_over():
            i = len(self.fbs)
            self.guesses[i] = guessed_code

            if len(guessed_code) == self.pegs:
                blacks = sum(g == c for g, c in zip(guessed_code, self.code))
                whites = sum((Counter(guessed_code) & Counter(
                    self.code)).values()) - blacks

                self.fbs[i] = Feedback(blacks, whites)

                if blacks == self.pegs:
                    self.won = True

    def guess_record(self):
        """Return a dictionary of guesses the player has made in the game.

        key: Turn number(0-based)
        value: Guessed code as a tuple of integers
        """
        return self.guesses

    def fb_record(self):
        """Return a dictionary of feedback on the guesses the player has
        made in the game.

        key: Turn number(0-based)
        value: Feedback of guessed code as a tuple of integers
        representing the number of black and white pegs.
        """
        return self.fbs
