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

pygame.display.update()


while not game.game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
