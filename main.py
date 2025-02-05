import pygame
from table import Table
from settings import WIDTH, HEIGTH, GREEN, BLACK


pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGTH))
font = pygame.font.Font(None, 36)
table = Table()

while not table.check_win() and table.turns_played < 64:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            table.handle_click(*event.pos)

    display.fill(BLACK)
    table.draw(display)
    turns = font.render("Turnos Jugados: %s" %(int(table.turns_played)), True, GREEN)
    display.blit(turns, (10, 10))
    pygame.display.flip()
pygame.quit()
