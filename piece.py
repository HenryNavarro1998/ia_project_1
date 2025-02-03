import pygame
from settings import BLACK

class Piece:
    def __init__(self, player, color=None, x=None, y=None, is_queen=False):
        self.player = player
        self.color = color
        self.x = x
        self.y = y
        self.is_queen = is_queen

    def __eq__(self, value):
        if isinstance(value, Piece):
            return self.player == value.player
        return False

    def draw(self, display):
        pos_x = self.x * 100 + 50
        pos_y = self.y * 100 + 50
        pygame.draw.circle(display, self.color, (pos_y, pos_x), 40)

        if self.is_queen:
            pygame.draw.circle(display, BLACK, (pos_y, pos_x), 15)
