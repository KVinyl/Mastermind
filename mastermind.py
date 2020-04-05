from collections import Counter, namedtuple
from random import randint


Feedback = namedtuple('Feedback', ['blacks', 'whites'])


class Mastermind():
    def __init__(self, pegs=4, colors=6, turns=12):
        self.pegs = pegs
        self.colors = colors
        self.turns = turns

        self.code = tuple(randint(1, self.colors) for _ in range(self.pegs))
        self.guesses = {}
        self.fbs = {}
        self.won = False

    def victory(self):
        return self.won

    def game_over(self):
        return self.victory() or len(self.guesses) == self.turns

    def guess(self, guessed_code):
        if not self.game_over():
            i = len(self.guesses)
            self.guesses[i] = guessed_code

            blacks = sum(g == c for g, c in zip(guessed_code, self.code))
            whites = sum((Counter(guessed_code) & Counter(
                self.code)).values()) - blacks

            self.fbs[i] = Feedback(blacks, whites)

            if blacks == self.pegs:
                self.won = True

    def last_fb(self):
        return self.fbs[len(self.fbs)-1] if self.fbs else None

    def guess_record(self):
        return self.guesses

    def fb_record(self):
        return self.fbs
