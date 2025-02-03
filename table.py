
from piece import Piece
from settings import WIDTH, HEIGTH, WHITE, BLACK, RED, BLUE
import pygame
import random
import copy

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
                    e, p, m = minimax(self, 5)

                if self._is_capture_move(pos_x, pos_y):
                    self.capture(pos_x,pos_y)
                    self.move(pos_x, pos_y)
                    self.turn = "x" if self.turn == "o" else "o"
                    e, p, m = minimax(self, 5)



    def check_win(self):
        red_count = sum(r.count(Piece("o")) for r in self.board)
        blue_count = sum(r.count(Piece("x")) for r in self.board)
        return 0 in [red_count, blue_count]


    def evaluate_board(self, to_eval=None):
        if  not to_eval:
            to_eval = self
        red_count = sum(r.count(Piece("o")) for r in to_eval.board)
        blue_count = sum(r.count(Piece("x")) for r in to_eval.board)
        return red_count - blue_count, None, None


    def get_pieces(self, board, player):
        return [
            piece for r in board for piece in r
            if piece and piece.player == player
        ]


    def get_valid_moves(self, piece):
        MOVES = [(-1,-1), (-1,1), (1,-1), (1,1), (-2,-2), (-2,2), (2,-2), (2,2)]
        valid_moves = []

        for move in MOVES:

            if (piece.x + move[0]) < 0 or (piece.x + move[0]) >= 4 or (piece.y + move[1]) < 0 or (piece.y + move[1]) >= 4:
                continue

            if not piece.is_queen:
                if piece.player == "x":
                    if (piece.x + move[0]) >= piece.x:
                        continue
                elif piece.player == "o":
                    if (piece.x + move[0]) <= piece.x:
                        continue
            valid_moves.append(move)
        return valid_moves

def minimax(board, depth, alpha=float("-inf"), beta=float("inf"), max_player=True):
        if depth == 0 or board.check_win():
            return board.evaluate_board(board)

        new_board = Table()
        new_board.board = board.board
        new_board.turn = board.turn
        new_board.piece = board.piece

        best_move = None
        piece_to_move = None
        if max_player:
            max_eval = float("-inf")
            pieces = board.get_pieces(board.board, "o")
            for piece in pieces:
                for move in board.get_valid_moves(piece):
                    board.handle_click(piece.y * 100, piece.x * 100)
                    board.handle_click((piece.y + move[0]) * 100, (piece.x + move[1]) * 100)

                    e, _p, _m = minimax(new_board, depth-1, alpha, beta, False)

                    if e > max_eval:
                        max_eval = e
                        piece_to_move = piece
                        best_move = move
                    alpha = max(alpha, e)

                    if beta <= alpha:
                        break
            return max_player, piece_to_move, best_move
        else:
            min_eval = float("inf")
            pieces = board.get_pieces(board.board, "x")
            for piece in pieces:
                for move in board.get_valid_moves(piece):
                    board.handle_click(piece.y * 100, piece.x * 100)
                    board.handle_click((piece.y + move[0]) * 100, (piece.x + move[1]) * 100)

                    e, _p, _m = minimax(new_board, depth-1, alpha, beta, True)

                    if e < min_eval:
                        min_eval = e
                        piece_to_move = piece
                        best_move = move
                    alpha = min(alpha, e)

                    if beta <= alpha:
                        break
            return min_eval, piece_to_move, best_move




