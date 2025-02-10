"""
Script principal del juego. Maneja la lógica del juego, turnos y eventos de Pygame.
"""
from utils import init_board, handle_move, is_game_over, generate_moves
from minimax import minimax
from layout import draw_board, get_clicked_position, GREEN
import pygame

GRID_SIZE = 500  # Tamaño de la ventana

# Inicialización del tablero
board = init_board()


def do_minimax_move(board):
    """Realiza un movimiento para el jugador 'x' usando Minimax o selección aleatoria."""
    valid_moves = generate_moves(board, "x")
    if not valid_moves:
        return board
    _, move = minimax(board, 3, float("-inf"), float("inf"), True)
    return handle_move(board, move)


# Configuración de Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE, GRID_SIZE))
pygame.display.set_caption("Checkers and Q-Learning")
font = pygame.font.Font(None, 36)
turn = "x"  # Turno inicial: jugador humano ("x")
selected_piece = None  # Pieza seleccionada por el jugador
running = False
turns_played = 0

# Bucle principal del juego
while not running and turns_played < 64:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True  # Salir del juego

        # Manejo de clics del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = get_clicked_position(event.pos)
            if click_x < 0 or click_x >= 4 or click_y < 0 or click_y >= 4:
                continue

            if not board[click_x][click_y] and selected_piece and (click_x, click_y) in [move[1] for move in generate_moves(board, "x") if move[0] == selected_piece]:
                # Mover pieza seleccionada
                board = handle_move(board, (selected_piece, (click_x, click_y)))
                selected_piece = None
                turn = "o"  # Cambiar turno a la IA
                turns_played += 1
            elif board[click_x][click_y] and board[click_x][click_y].lower() == "x":
                selected_piece = (click_x, click_y)  # Seleccionar pieza

    # Turno de la IA
    running, _ = is_game_over(board)

    if turn == "o" and not running:
        board = do_minimax_move(board)
        turn = "x"

    # Actualizar interfaz y verificar fin del juego
    draw_board(screen, board, selected_piece)
    turns = font.render("Turnos Jugados: %s" %(turns_played), True, GREEN)
    screen.blit(turns, (10, 10))
    pygame.display.flip()