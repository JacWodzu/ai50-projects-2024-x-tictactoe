import pygame
import math
from sklearn.tree import DecisionTreeClassifier


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count > o_count:
        return O
    else:
        return X # Xgoes first
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    #Deep copy the board
    new_board = [row[:] for row in board]        
    current_player = player(board)
    new_board[action[0]][action[1]] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows and columns for winners
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    
    # Check diagonals for winners
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None
    


def terminal(board):
    ## Check rows
    #for i in range(3):
    #   if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ':
    #       return board[i][0]
    
    ## Check columns
    #for i in range(3):
    #   if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ':
    #       return board[0][i]
    
    ## Check diagonals
    #if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
    #   return board[0][0]
    
    #if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
    #   return board[0][2]
    
    ## Check for empty spaces
    #for row in board:
    #   for cell in row:
    #       if cell == ' ':
    #           return 'ongoing'
    
    # If no winner and no empty spaces, return tie
    #return 'tie'
    
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


#def minimax(board, player):
    #if check_winner(board, 'X'):
    #    return -1
    #elif check_winner(board, 'O'):
    #    return 1
    #elif check_draw(board):
    #    return 0

    #if player == 'O':
    #    best_score = -float('inf')
    #    for move in available_moves(board):
    #        board[move] = player
    #        score = minimax(board, 'X')
    #        board[move] = ' '
    #        best_score = max(score, best_score)
    #else:
    #    best_score = float('inf')
    #    for move in available_moves(board):
    #       board[move] = player
    #       score = minimax(board, 'O')
    #       board[move] = ' '
    #       best_score = min(score, best_score)

    #return best_score

def minimax(board):
    """
    Returns the optimal move for the player to move on the board.
    """
    if terminal(board):
        return None

    #current_player = player(board)

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
   

def best_move(board):
    best_score = -float('inf')
    best_move = None

    for move in available_moves(board):
        board[move] = 'O'
        score = minimax(board, 'X')
        board[move] = ' '

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        current_player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == current_player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != current_player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == current_player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
