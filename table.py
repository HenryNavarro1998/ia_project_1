
from piece import Piece
from settings import WIDTH, HEIGTH, WHITE, BLACK, RED, BLUE
import pygame
import random
from minimax import minimax

def validate_direction(func):
    def wrapper(self, pos_x, pos_y):
        # Verificar si la pieza existe
        if not self.piece:
            return False

        print("pos x:", pos_x)
        print("pos y:", pos_y)

        # Verificar que las posiciones estén dentro del tablero (0 a 3 para un tablero de 4x4)
        # if not (0 < pos_x <= 4)  and not 0 < pos_y <= 4:
        if pos_x < 0 or pos_x >= 4 or pos_y < 0 or pos_y >= 4:
            print("Posición fuera del tablero.")
            return False

        # Verificar si la pieza es una reina
        if not self.piece.is_queen:
            # Verificar la dirección del movimiento
            if self.piece.player == "x":  # Jugador 1 (movimiento hacia adelante)
                if pos_x >= self.piece.x:
                    print("Movimiento inválido: el jugador 1 solo puede moverse hacia adelante.")
                    return False
            elif self.piece.player == "o":  # Jugador 2 (movimiento hacia adelante)
                if pos_x <= self.piece.x:
                    print("Movimiento inválido: el jugador 2 solo puede moverse hacia adelante.")
                    return False

        # Si todas las validaciones pasan, ejecutar la función original
        return func(self, pos_x, pos_y)
    return wrapper

class Table:
    def __init__(self):
        self.board = self.init_board()
        # display = pygame.display.set_mode((WIDTH, HEIGTH))
        self.piece = None
        # self.turn = random.choice(["x","o"])
        self.turn = "x"


    def init_board(self):
        board = [[None for _ in range(4)] for _ in range(4)]
        board[0][1] = Piece("o", RED, 0, 1)
        board[0][3] = Piece("o", RED, 0, 3)
        board[3][0] = Piece("x", BLUE, 3, 0)
        board[3][2] = Piece("x", BLUE, 3, 2)
        return board

    # def copy(self):
    #     return Table(copy.deepcopy(self))

    def draw(self, display):
        for i in range(4):
            for j in range(4):
                color = WHITE if (j+i) % 2 == 0 else BLACK
                dimensions = (j * 100, i * 100, 100, 100)
                pygame.draw.rect(display, color, dimensions)

                if self.board[i][j]:
                    self.board[i][j].draw(display)

    @validate_direction
    def _is_single_move(self, pos_x, pos_y):
        if not self.piece:
            return False
        return abs(self.piece.x - pos_x) == 1 and abs(self.piece.y - pos_y) == 1

    @validate_direction
    def _is_capture_move(self, pos_x, pos_y):
        if not self.piece:
            return False

        x, y = self.piece.x, self.piece.y
        mid_x = (x + pos_x) // 2
        mid_y = (y + pos_y) // 2

        if abs(x - pos_x) != 2 or abs(y - pos_y) != 2:
            return False

        if not self.board[mid_x][mid_y]:
            return False

        if self.piece.player == self.board[mid_x][mid_y].player:
            return False

        return True


    def get_board(self):
        board = [[None for _ in range(4)] for _ in range(4)]

        for r in range(4):
            for c in range(4):
                if self.board[r][c]:
                    board[r][c] = self.board[r][c].player
                    if self.board[r][c].is_queen:
                        board[r][c] = board[r][c].upper()

        return board



    def move(self, x, y):
        piece_x = self.piece.x
        piece_y = self.piece.y
        self.board[piece_x][piece_y] = None

        if self.piece.player == "x" and x == 0 or self.piece.player == "o" and x == 3:
            self.piece.is_queen = True

        self.board[x][y] = Piece(
            self.piece.player, self.piece.color, x, y, self.piece.is_queen
        )


        self.piece = None
        return


    def capture(self, x, y):
        mid_x = (self.piece.x + x) // 2
        mid_y = (self.piece.y + y) // 2

        self.board[mid_x][mid_y] = None
        return

    def handle_click(self, click_y, click_x):

        pos_x = click_x // 100
        pos_y = click_y // 100

        pos_cell = self.board[pos_x][pos_y]


        #Seleccionar una ficha
        if pos_cell and pos_cell.player == self.turn:
            self.piece = pos_cell
            return


        if self.piece:
            if not pos_cell:

                if self._is_single_move(pos_x, pos_y):
                    self.move(pos_x, pos_y)
                    self.turn = "x" if self.turn == "o" else "o"
                    e, m = minimax(self.get_board(), 3, float("-inf"), float("inf"), True)
                    piece, move = m[0], m[1]
                    self.handle_click(piece[1] * 100, piece[0] * 100)
                    self.handle_click(move[1] * 100, move[0] * 100)


                if self._is_capture_move(pos_x, pos_y):
                    self.capture(pos_x,pos_y)
                    self.move(pos_x, pos_y)
                    self.turn = "x" if self.turn == "o" else "o"
                    e, m = minimax(self.get_board(), 3, float("-inf"), float("inf"), True)
                    piece, move = m[0], m[1]
                    self.handle_click(piece[1] * 100, piece[0] * 100)
                    self.handle_click(move[1] * 100, move[0] * 100)


    def check_win(self):
        red_count = sum(r.count(Piece("o")) for r in self.board)
        blue_count = sum(r.count(Piece("x")) for r in self.board)
        return 0 in [red_count, blue_count]

