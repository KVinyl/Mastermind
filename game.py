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
DARKEST_GRAY = (48, 48, 48)
BLUE_GREEN = (13, 152, 186)


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

SQUARESIZE = 60
pegsize = SQUARESIZE//3

width = SQUARESIZE * (pegs + 2)
height = SQUARESIZE * (turns + 3)

screen = pygame.display.set_mode((width, height), 0, 32)
screen.fill(DARK_GRAY)
pygame.display.set_caption('Mastermind')

divider = height - 2 * SQUARESIZE


class GuessButton():
    def __init__(self, color_int, x, y, radius):
        self.color_int = color_int
        self.x = x
        self.y = y
        self.radius = radius

    def color_code(self):
        return self.color_int

    def draw(self):
        pygame.draw.circle(
            screen, color_tran[self.color_int], (self.x, self.y), self.radius)

    def is_over(self, pos):
        return (pos[0] - self.x)**2 + (pos[1] - self.y)**2 <= self.radius**2


class RectButton():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))

        if self.text != '':
            font = pygame.font.SysFont('arial', 40)
            text = font.render(self.text, 1, WHITE)
            screen.blit(text, (self.x + (self.width//2-text.get_width()//2),
                               self.y + (self.height//2-text.get_height()//2)))

    def is_over(self, pos):
        return (pos[0] > self.x and pos[0] < self.x + self.width
                and pos[1] > self.y and pos[1] < self.y + self.height)


def draw_lines(turns):
    pygame.draw.line(screen, GRAY, (width - SQUARESIZE,
                                    0), (width - SQUARESIZE, divider-1))
    for t in range(2, turns+1):
        y = t * SQUARESIZE
        pygame.draw.line(screen, GRAY, (SQUARESIZE, y), (width, y))


def draw_guess_buttons(colors):
    buttons = []

    y = divider + SQUARESIZE//2
    radius = pegsize

    pygame.draw.rect(screen, DARKEST_GRAY,
                     (0, height-SQUARESIZE*2, width, SQUARESIZE*2))
    for c in range(1, colors+1):
        x = (c-1) * SQUARESIZE + SQUARESIZE // 2
        color_button = GuessButton(c, x, y, radius)
        color_button.draw()
        buttons.append(color_button)

    return buttons


def draw_guess(guess_record, turn):
    guess = (0, 0, 0, 0)
    if turn in guess_record and guess_record[turn]:
        guess = guess_record[turn]

    for i, peg in enumerate(guess, 1):
        x = i * SQUARESIZE + SQUARESIZE // 2
        y = divider - (turn * SQUARESIZE + SQUARESIZE // 2)
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
        y = (divider - ((turn+1) * SQUARESIZE)) + \
            SQUARESIZE//4 + i//2 * SQUARESIZE//2
        radius = SQUARESIZE // 6

        pygame.draw.circle(screen, key_tran[peg], (x, y), radius)


def draw_left_col(n=None):
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, SQUARESIZE, divider))

    y = 0 if n is None else height - (SQUARESIZE * (n + 3))

    x1, y1 = SQUARESIZE//6, y + SQUARESIZE//6
    x2, y2 = x1, y + SQUARESIZE*5//6
    x3, y3 = SQUARESIZE*5//6, y+SQUARESIZE//2
    pygame.draw.polygon(screen, BLUE_GREEN, [
                        (x1, y1), (x2, y2), (x3, y3)])

    pygame.display.update()


def draw_board(guess_record, fb_record):
    for turn in range(turns):
        draw_guess(guess_record, turn)
        draw_feedback(fb_record, turn)

    draw_left_col(len(fb_record))

    pygame.display.update()


def draw_top_bar(code=None):
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, width, SQUARESIZE))
    if code is None:
        pygame.draw.rect(screen, DARKEST_GRAY, (SQUARESIZE, 0,
                                                pegs * SQUARESIZE, SQUARESIZE))
    else:
        for i, peg in enumerate(code, 1):
            x = i * SQUARESIZE + SQUARESIZE // 2
            y = SQUARESIZE // 2
            radius = pegsize

            pygame.draw.circle(screen, color_tran[peg], (x, y), radius)

    pygame.display.update()


def game():
    mastermind = Mastermind(pegs, colors, turns)

    guess_buttons = draw_guess_buttons(colors)

    clear = RectButton(RED, 0, divider + SQUARESIZE,
                       width//2, SQUARESIZE, 'CLEAR')
    submit = RectButton(GREEN, width//2, divider + SQUARESIZE,
                        width//2, SQUARESIZE, 'SUBMIT')
    clear.draw()
    submit.draw()

    draw_lines(turns)
    draw_board(mastermind.guess_record(), mastermind.fb_record())
    draw_top_bar()

    guessed_code = []
    while not mastermind.game_over():
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pos[1] >= divider:
                    # Checks if the clear button was clicked
                    if clear.is_over(pos):
                        guessed_code.clear()
                        mastermind.guess(guessed_code, submitted=False)

                    # Checks if the submit button was clicked
                    elif submit.is_over(pos):
                        mastermind.guess(guessed_code)
                        if len(guessed_code) == pegs:
                            guessed_code.clear()

                    # Checks if a guess button was clicked
                    else:
                        for button in guess_buttons:
                            if button.is_over(pos):
                                if len(guessed_code) < pegs:
                                    guessed_code.append(button.color_code())

                                mastermind.guess(
                                    guessed_code, submitted=False)
                                break

                    draw_board(mastermind.guess_record(),
                               mastermind.fb_record())

    draw_top_bar(mastermind.reveal_code())
    draw_left_col()


def main():
    while True:
        game()

        new_game = RectButton(GREEN, 0, divider + SQUARESIZE,
                              width, SQUARESIZE, 'NEW GAME')
        new_game.draw()
        pygame.display.update()

        restart = False
        while not restart:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if new_game.is_over(pos):
                        restart = True
                        break


if __name__ == '__main__':
    main()
