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
ORANGE = (255, 100, 0)
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
pegsize = SQUARESIZE//3

width = SQUARESIZE * (pegs + 2)
height = SQUARESIZE * (turns + 2)

screen = pygame.display.set_mode((width, height), 0, 32)
screen.fill(DARK_GRAY)
pygame.display.set_caption('Mastermind')


class GuessButton():
    def __init__(self, color, x, y, radius):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius

    def color_code(self):
        return self.color

    def draw(self):
        pygame.draw.circle(
            screen, color_tran[self.color], (self.x, self.y), self.radius)

    def is_over(self, mouse_pos):
        return (pos[0] - self.x)**2 + (pos[1] - self.y)**2 <= self.radius**2


def draw_guess_buttons(colors):
    buttons = []

    y = height - SQUARESIZE//2
    radius = pegsize

    pygame.draw.rect(screen, BLACK, (0, height-SQUARESIZE, width, SQUARESIZE))
    for c in range(1, colors+1):
        x = (c-1) * SQUARESIZE + SQUARESIZE // 2
        color_button = GuessButton(c, x, y, radius)
        color_button.draw()
        buttons.append(color_button)

    return buttons


def draw_guess(guess_record, turn):
    guess = (0, 0, 0, 0)
    if turn in guess_record:
        guess = guess_record[turn]

    for i, peg in enumerate(guess, 1):
        x = i * SQUARESIZE + SQUARESIZE // 2
        y = height - ((turn+1) * SQUARESIZE + SQUARESIZE // 2)
        radius = pegsize

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


guess_buttons = draw_guess_buttons(colors)
draw_board(game.guess_record(), game.fb_record())

guessed_code = []
while not game.game_over():
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pos[1] >= height-SQUARESIZE:
                for button in guess_buttons:
                    if button.is_over(pos):
                        guessed_code.append(button.color_code())

                        game.guess(tuple(guessed_code))
                        draw_board(game.guess_record(), game.fb_record())
                        if len(guessed_code) == pegs:
                            guessed_code.clear()

                        break

print('You win!') if game.victory() else print('You lose.')
pygame.time.wait(3000)
