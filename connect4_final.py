import numpy as np
import pygame
import sys
import math
import random

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True, [(r, c), (r, c + 1), (r, c + 2), (r, c + 3)]

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True, [(r, c), (r + 1, c), (r + 2, c), (r + 3, c)]

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True, [(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)]

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True, [(r, c), (r - 1, c + 1), (r - 2, c + 2), (r - 3, c + 3)]

    return False, []

def highlight_winning_move(winning_coords, piece):
    highlight_color = WHITE  # Use white to highlight the winning pieces
    for (r, c) in winning_coords:
        pygame.draw.circle(
            screen,
            highlight_color,
            (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)),
            RADIUS + 10,  # Slightly larger radius for highlighting
            5  # Thickness of the highlight circle
        )
    pygame.display.update()  # Ensure the screen is updated

def draw_board(board):
    # Draw the board grid and empty slots
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    # Draw the pieces on the board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    pygame.display.update()

def play_again():
    global board, game_over, turn
    board = create_board()
    game_over = False
    turn = 0
    draw_board(board)
    pygame.display.update()

# Display scores at the top of the screen
def display_scores(player1_score, player2_score):
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Clear the top area
    small_font = pygame.font.SysFont("monospace", 30)  # Use a smaller font size
    score_label = small_font.render(f"Player 1: {player1_score}  Player 2: {player2_score}", 1, WHITE)
    screen.blit(score_label, (40, 10))  # Adjust position if needed
    pygame.display.update()

def choose_game_mode():
    pygame.draw.rect(screen, BLACK, (0, 0, width, height))  # Clear the screen
    font = pygame.font.SysFont("monospace", 35)  # Reduced font size
    label1 = font.render("Press 1 for Player vs Player", 1, WHITE)
    label2 = font.render("Press 2 for Player vs AI", 1, WHITE)
    screen.blit(label1, (40, height // 2 - 100))
    screen.blit(label2, (40, height // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "PvP"
                elif event.key == pygame.K_2:
                    return "PvAI"

# Initialize scores
player1_score = 0
player2_score = 0

# Main game loop
while True:  # Main loop to allow replaying the game
    pygame.init()

    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)
    RADIUS = int(SQUARESIZE / 2 - 5)

    # Initialize the screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect 4")

    # Choose game mode
    game_mode = choose_game_mode()

    # Create the board and reset game state
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    # Draw the initial board
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    # Display initial scores
    display_scores(player1_score, player2_score)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Highlight the column where the player is hovering (PvP only)
            if event.type == pygame.MOUSEMOTION and game_mode == "PvP":
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                display_scores(player1_score, player2_score)  # Update scores
                pygame.display.update()

            # Handle mouse click for column selection (PvP)
            if event.type == pygame.MOUSEBUTTONDOWN and game_mode == "PvP":
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, turn + 1)

                    if winning_move(board, turn + 1)[0]:
                        winning_coords = winning_move(board, turn + 1)[1]
                        label = myfont.render(f"Player {turn + 1} wins!!", 1, RED if turn == 0 else YELLOW)
                        screen.blit(label, (40, 10))
                        pygame.display.update()

                        draw_board(board)
                        highlight_winning_move(winning_coords, turn + 1)
                        pygame.time.wait(5000)
                        game_over = True

                        if turn == 0:
                            player1_score += 1
                        else:
                            player2_score += 1

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            # Handle keyboard input for column selection (PvP)
            if event.type == pygame.KEYDOWN and game_mode == "PvP":
                if pygame.K_1 <= event.key <= pygame.K_7:  # Keys 1 to 7
                    col = event.key - pygame.K_1  # Map keys 1-7 to columns 0-6

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, turn + 1)

                        if winning_move(board, turn + 1)[0]:
                            winning_coords = winning_move(board, turn + 1)[1]
                            label = myfont.render(f"Player {turn + 1} wins!!", 1, RED if turn == 0 else YELLOW)
                            screen.blit(label, (40, 10))
                            pygame.display.update()

                            draw_board(board)
                            highlight_winning_move(winning_coords, turn + 1)
                            pygame.time.wait(5000)
                            game_over = True

                            if turn == 0:
                                player1_score += 1
                            else:
                                player2_score += 1

                        print_board(board)
                        draw_board(board)

                        turn += 1
                        turn = turn % 2

        # AI's turn (PvAI)
        if game_mode == "PvAI" and turn == 1 and not game_over:
            pygame.time.wait(1000)  # Add a delay for the AI's move
            col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)  # Depth = 4

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2)[0]:
                    winning_coords = winning_move(board, 2)[1]
                    label = myfont.render("AI wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    pygame.display.update()

                    draw_board(board)
                    highlight_winning_move(winning_coords, 2)
                    pygame.time.wait(5000)
                    game_over = True

                    player2_score += 1

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        # Player's turn in PvAI
        if game_mode == "PvAI" and turn == 0 and not game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_7:  # Keys 1 to 7
                        col = event.key - pygame.K_1  # Map keys 1-7 to columns 0-6

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)

                            if winning_move(board, 1)[0]:
                                winning_coords = winning_move(board, 1)[1]
                                label = myfont.render("Player 1 wins!!", 1, RED)
                                screen.blit(label, (40, 10))
                                pygame.display.update()

                                draw_board(board)
                                highlight_winning_move(winning_coords, 1)
                                pygame.time.wait(5000)
                                game_over = True

                                player1_score += 1

                            print_board(board)
                            draw_board(board)

                            turn += 1
                            turn = turn % 2

        # Update scores after every event
        display_scores(player1_score, player2_score)

        if game_over:
            pygame.time.wait(3000)

            # Prompt for play again
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            play_again_label = myfont.render("Press R to Play Again or Q to Quit", 1, WHITE)
            screen.blit(play_again_label, (40, 10))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Restart the game
                            play_again()
                            waiting = False
                        elif event.key == pygame.K_q:  # Quit the game
                            pygame.quit()
                            sys.exit()