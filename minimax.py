def evaluate_board(board):
    red_count = sum(row.count("o") for row in board) + (sum(row.count("O") for row in board) * 2)
    blue_count = sum(row.count("x") for row in board) + (sum(row.count("X") for row in board) * 2)
    return red_count - blue_count


def check_win(board):
    red_count = sum(row.count("o") for row in board) + sum(row.count("O") for row in board)
    blue_count = sum(row.count("x") for row in board) + sum(row.count("X") for row in board)
    return red_count == 0 or blue_count == 0


def generate_moves(board, player):
    moves = []
    for r in range(4):
        for c in range(4):
            if board[r][c] == player or board[r][c] == player.upper():  # Incluye reinas
                is_queen = board[r][c] == player.upper()  # Verifica si es una reina
                for x, y in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                    # Verifica si el movimiento es hacia adelante o si es una reina
                    if player == 'o':
                        if x == -1 and not is_queen:  # 'o' solo puede moverse hacia abajo (x = 1)
                            continue
                    elif player == 'x':
                        if x == 1 and not is_queen:  # 'x' solo puede moverse hacia arriba (x = -1)
                            continue

                    to_x, to_y = (r + x, c + y)
                    if 0 <= to_x < 4 and 0 <= to_y < 4 and board[to_x][to_y] is None:
                        moves.append(((r, c), (to_x, to_y)))

                    capture_r, capture_c = ((r + x * 2), (c + y * 2))

                    if (0 <= capture_r < 4 and 0 <= capture_c < 4 and
                        board[capture_r][capture_c] is None and
                        board[to_x][to_y] is not None and
                        board[to_x][to_y] != player and board[to_x][to_y] != player.upper()):

                        moves.append(((r, c), (capture_r, capture_c)))
    return moves


def generate_new_board(board, move):
    temp_board = [r[:] for r in board]  # Copia profunda del tablero
    (r, c), (to_r, to_c) = move
    piece = temp_board[r][c]
    
    # Mueve la ficha
    temp_board[r][c] = None
    temp_board[to_r][to_c] = piece

    # Elimina ficha capturada en saltos
    if abs(to_r - r) == 2:
        captured_r = (r + to_r) // 2
        captured_c = (c + to_c) // 2
        temp_board[captured_r][captured_c] = None

    # Coronación de fichas (convertir a mayúscula)
    if piece in ['o', 'x']:  # Solo aplica a fichas no coronadas
        if (piece == 'o' and to_r == 3) or (piece == 'x' and to_r == 0):
            temp_board[to_r][to_c] = piece.upper()  # Convertir en reina

    return temp_board

def minimax(board, depth, alpha, beta, player):
    if not depth or check_win(board):
        return evaluate_board(board), None

    best_move = None
    if player:
        max_eval = float("-inf")
        for move in generate_moves(board, "o"):
            temp_board = generate_new_board(board, move)
            ev, _ = minimax(temp_board, depth-1, alpha, beta, False)
            if ev > max_eval:
                max_eval = ev
                best_move = move
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for move in generate_moves(board, "x"):
            temp_board = generate_new_board(board, move)
            ev, _ = minimax(temp_board, depth-1, alpha, beta, True)
            if ev < min_eval:
                min_eval = ev
                best_move = move
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval, best_move
