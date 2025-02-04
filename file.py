# import pygame
# import random


# #Screen Dimensions
# WIDTH = HEIGTH = 400

# #Colors
# BLACK = (0,0,0)
# WHITE = (255,255,255)
# RED = (255,0,0)
# BLUE = (0,0,255)



# class Piece:
#     def __init__(self, player, color, x, y, is_queen=False):
#         self.player = player
#         self.color = color
#         self.x = x
#         self.y = y
#         self.is_queen = is_queen

#     def draw(self, display):
#         pos_x = self.x * 100 + 50
#         pos_y = self.y * 100 + 50
#         pygame.draw.circle(display, self.color, (pos_y, pos_x), 40)

#         if self.is_queen:
#             pygame.draw.circle(display, BLACK, (pos_y, pos_x), 15)


# def _init_board():
#     board = [[None for _ in range(4)] for _ in range(4)]
#     board[0][1] = Piece("o", RED, 0, 1)
#     board[0][3] = Piece("o", RED, 0, 3)
#     board[3][0] = Piece("x", BLUE, 3, 0)
#     board[3][2] = Piece("x", BLUE, 3, 2)
#     return board

# def validate_direction(func):
#     def wrapper(self, pos_x, pos_y):
#         if not self.piece:
#             return False

#         print("pos x", pos_x)
#         print("pos y", pos_y)
#         # Verificar si la pieza es una reina
#         if not self.piece.is_queen:
#             # Verificar la dirección del movimiento
#             if self.piece.player == "x":  # Jugador 1 (movimiento hacia adelante)
#                 if pos_x >= self.piece.x:
#                     return False
#             elif self.piece.player == "o":  # Jugador 2 (movimiento hacia adelante)
#                 if pos_x <= self.piece.x:
#                     return False

#         return func(self, pos_x, pos_y)
#     return wrapper

# class Table:
#     def __init__(self):
#         self.board = _init_board()
#         self.display = pygame.display.set_mode((WIDTH, HEIGTH))
#         self.piece = None
#         self.turn = random.choice(["x","o"])

#     def draw(self):
#         for i in range(4):
#             for j in range(4):
#                 color = WHITE if (j+i) % 2 == 0 else BLACK
#                 dimensions = (j * 100, i * 100, 100, 100)
#                 pygame.draw.rect(self.display, color, dimensions)

#                 if self.board[i][j]:
#                     self.board[i][j].draw(self.display)

#     @validate_direction
#     def _is_single_move(self, pos_x, pos_y):
#         if not self.piece:
#             return False
#         return abs(self.piece.x - pos_x) == 1 and abs(self.piece.y - pos_y) == 1

#     @validate_direction
#     def _is_capture_move(self, pos_x, pos_y):
#         if not self.piece:
#             return False

#         x, y = self.piece.x, self.piece.y
#         mid_x = (x + pos_x) // 2
#         mid_y = (y + pos_y) // 2

#         if abs(x - pos_x) != 2 or abs(y - pos_y) != 2:
#             return False

#         if not self.board[mid_x][mid_y]:
#             return False

#         if self.piece.player == self.board[mid_x][mid_y].player:
#             return False

#         return True


#     def move(self, x, y):
#         piece_x = self.piece.x
#         piece_y = self.piece.y
#         self.board[piece_x][piece_y] = None

#         if self.piece.player == "x" and x == 0 or self.piece.player == "o" and x == 3:
#             self.piece.is_queen = True

#         self.board[x][y] = Piece(
#             self.piece.player, self.piece.color, x, y, self.piece.is_queen
#         )


#         self.piece = None
#         return


#     def capture(self, x, y):
#         mid_x = (self.piece.x + x) // 2
#         mid_y = (self.piece.y + y) // 2

#         self.board[mid_x][mid_y] = None
#         return

#     def handle_click(self, click_y, click_x):

#         pos_x = click_x // 100
#         pos_y = click_y // 100

#         pos_cell = self.board[pos_x][pos_y]

#         #Seleccionar una ficha
#         if pos_cell and pos_cell.player == self.turn:
#             print("Seleccionaste la ficha en: (%s, %s, %s)"
#                 %(pos_cell.player, pos_cell.x, pos_cell.y)
#             )
#             self.piece = pos_cell
#             return


#         if self.piece:
#             if not pos_cell:

#                 if self._is_single_move(pos_x, pos_y):
#                     print("Te moviste")
#                     self.move(pos_x, pos_y)
#                     self.turn = "x" if self.turn == "o" else "o"

#                 if self._is_capture_move(pos_x, pos_y):
#                     print("Capturaste")
#                     self.capture(pos_x,pos_y)
#                     self.move(pos_x, pos_y)


# pygame.init()
# table = Table()

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             vert, hor = event.pos
#             print("Vert: %s - Hor: %s" %(vert, hor))
#             table.handle_click(*event.pos)

#     # table.check_win()
#     table.display.fill(BLACK)
#     table.draw()
#     pygame.display.flip()
# pygame.quit()


def fun(a):
    a = a +5

var = 5
fun(var)
print(var)