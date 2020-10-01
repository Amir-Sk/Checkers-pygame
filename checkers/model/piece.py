from services.constants import  WHITE, BLACK, SQUARE_SIZE, BLUE
import pygame


class Piece:

    PADDING = 10
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.calc_position()

    def calc_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        coords = (self.x, self.y)
        pygame.draw.circle(win, BLUE, coords, radius+self.OUTLINE)
        pygame.draw.circle(win, self.color, coords, radius)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_position()

    def __repr__(self):
        return str(self.color,)