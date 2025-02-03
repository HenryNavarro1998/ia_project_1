import pygame
from table import Table
from settings import WIDTH, HEIGTH, WHITE, BLACK

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGTH))
table = Table()

while not table.check_win():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            table.handle_click(*event.pos)

    display.fill(BLACK)
    table.draw(display)
    pygame.display.flip()
pygame.quit()
