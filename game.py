from mastermind import Mastermind

import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (96, 96, 96)

color_tran = {
    0: GRAY,
    1: RED,
    2: ORANGE,
    3: YELLOW,
    4: GREEN,
    5: BLUE,
    6: PURPLE
}

key_tran = {
    0: GRAY,
    1: WHITE,
    2: BLACK
}

pygame.init()

pegs = 4
colors = 6
turns = 12

game = Mastermind(pegs, colors, turns)

SQUARESIZE = 60

width = SQUARESIZE * (pegs + 2)
height = SQUARESIZE * (turns + 2)

screen = pygame.display.set_mode((width, height), 0, 32)
screen.fill(DARK_GRAY)
pygame.display.set_caption('Mastermind')


def draw_guess(guess_record, turn):
    guess = (0, 0, 0, 0)
    if turn in guess_record:
        guess = guess_record[turn]

    for i, peg in enumerate(guess, 1):
        x = i * SQUARESIZE + SQUARESIZE // 2
        y = height - ((turn+1) * SQUARESIZE + SQUARESIZE // 2)
        radius = SQUARESIZE // 4

        pygame.draw.circle(screen, color_tran[peg], (x, y), radius)


def draw_feedback(fb_record, turn):
    fb = (0, 0, 0, 0)
    if turn in fb_record:
        blacks = fb_record[turn].blacks
        whites = fb_record[turn].whites
        blanks = pegs - (blacks + whites)

        fb = tuple(blacks*[2] + whites*[1] + blanks*[0])

    for i, peg in enumerate(fb):
        x = (width - SQUARESIZE) + SQUARESIZE//4 + i % 2 * SQUARESIZE//2
        y = (height - ((turn+2) * SQUARESIZE)) + \
            SQUARESIZE//4 + i//2 * SQUARESIZE//2
        radius = SQUARESIZE // 6

        pygame.draw.circle(screen, key_tran[peg], (x, y), radius)


def draw_board(guess_record, fb_record):
    for turn in range(turns):
        draw_guess(guess_record, turn)
        draw_feedback(fb_record, turn)

    pygame.display.update()


draw_board(game.guess_record(), game.fb_record())

while not game.game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Guess is temporarily inputted by text
            guessed_code = tuple(int(n) for n in input('Enter guess: '))
            game.guess(guessed_code)
            draw_board(game.guess_record(), game.fb_record())

print('You win!') if game.victory() else print('You lose.')
pygame.time.wait(3000)
