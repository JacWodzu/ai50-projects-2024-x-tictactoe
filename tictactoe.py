import math
import pygame
import sys
import time

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return O if x_count > o_count else X

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    if action not in actions(board):
        raise ValueError("Invalid action")
    new_board = [row[:] for row in board]        
    current_player = player(board)
    new_board[action[0]][action[1]] = current_player
    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None

def terminal(board):
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None

    def minimax_helper(board, maximizing):
        if terminal(board):
            return utility(board)

        if maximizing:
            best_value = -math.inf
            for action in actions(board):
                value = minimax_helper(result(board, action), False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = math.inf
            for action in actions(board):
                value = minimax_helper(result(board, action), True)
                best_value = min(best_value, value)
            return best_value

    best_score = -math.inf
    best_action = None

    for action in actions(board):
        score = minimax_helper(result(board, action), False)
        if score > best_score:
            best_score = score
            best_action = action

    return best_action

pygame.init()

# Set up the game window
size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
tile_color = (200, 200, 200)

# Font configurations
mediumFont = pygame.font.Font(None, 28)
largeFont = pygame.font.Font(None, 40)
moveFont = pygame.font.Font(None, 60)

user = None
board = initial_state()
ai_turn = False

def draw_board(board):
    tile_size = 200  # Increase tile size for better visibility
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, tile_color, rect)
            pygame.draw.rect(screen, black, rect, 3)

            if board[i][j] != EMPTY:
                move = moveFont.render(board[i][j], True, black)
                moveRect = move.get_rect()
                moveRect.center = rect.center
                screen.blit(move, moveRect)

while True:
    screen.fill(white)  # Fill the screen with white background
    draw_board(board)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if user is None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 0 <= mouse[0] <= 300 and 250 <= mouse[1] <= 300:
                    user = X
                elif 300 < mouse[0] <= 600 and 250 <= mouse[1] <= 300:
                    user = O
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not terminal(board):
                mouse = pygame.mouse.get_pos()
                col = mouse[0] // 200
                row = mouse[1] // 200

                if board[row][col] == EMPTY and user == player(board):
                    board = result(board, (row, col))
                    if not terminal(board):
                        ai_turn = True

    # AI's turn
    if ai_turn:
        time.sleep(0.5)  # Pause for a moment to simulate thinking
        move = minimax(board)
        if move is not None:
            board = result(board, move)
        ai_turn = False

    # Check for win or tie
    if terminal(board):
        winner = winner(board)
        message = "It's a Tie!" if winner is None else f"{winner} wins!"
        text = mediumFont.render(message, True, black)
        screen.blit(text, (size[0] // 2 - text.get_width() // 2, size[1] // 2 - text.get_height() // 2))

    pygame.display.flip()  # Update the display
