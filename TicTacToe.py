import pygame
import sys
import time
import math
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
BOARD_SIZE = 3
CELL_SIZE = WINDOW_SIZE // BOARD_SIZE
LINE_WIDTH = 15
CIRCLE_WIDTH = 15
CROSS_WIDTH = 15
CIRCLE_RADIUS = CELL_SIZE // 3
CROSS_SPACE = CELL_SIZE // 4

# Enhanced Colors
BG_COLOR = (255, 255, 255)  # White background
GRID_COLOR = (200, 200, 200)  # Light gray grid
LINE_COLOR = (150, 150, 150)
CIRCLE_COLOR = (34, 139, 34)  # Green for O
CROSS_COLOR = (220, 20, 20)   # Red for X
TEXT_COLOR = (50, 50, 50)     # Dark gray text
HOVER_COLOR = (220, 220, 220, 128)  # Light gray hover

# Box Colors
PLAYER_X_COLOR = (255, 200, 200)  # Light red for X
PLAYER_O_COLOR = (200, 255, 200)  # Light green for O
EMPTY_BOX_COLOR = (255, 255, 255)  # White for empty boxes

# Set up display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Tic Tac Toe')

# Font setup
game_font = pygame.font.Font(None, 74)
info_font = pygame.font.Font(None, 36)

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'O'
        self.game_state = "playing"
        self.winner = None
        self.hover_cell = None
        self.box_colors = [[EMPTY_BOX_COLOR for _ in range(BOARD_SIZE)] 
                          for _ in range(BOARD_SIZE)]

    def draw_lines(self):
        # Draw grid lines
        for i in range(1, BOARD_SIZE):
            # Vertical lines
            pygame.draw.line(screen, GRID_COLOR,
                           (i * CELL_SIZE, 0),
                           (i * CELL_SIZE, WINDOW_SIZE),
                           2)
            # Horizontal lines
            pygame.draw.line(screen, GRID_COLOR,
                           (0, i * CELL_SIZE),
                           (WINDOW_SIZE, i * CELL_SIZE),
                           2)

    def draw_symbols(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                center = (int(col * CELL_SIZE + CELL_SIZE // 2),
                         int(row * CELL_SIZE + CELL_SIZE // 2))
                
                if self.board[row][col] == 'O':
                    pygame.draw.circle(screen, CIRCLE_COLOR,
                                    center, CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[row][col] == 'X':
                    x_start = col * CELL_SIZE + CROSS_SPACE
                    x_end = col * CELL_SIZE + CELL_SIZE - CROSS_SPACE
                    y_start = row * CELL_SIZE + CROSS_SPACE
                    y_end = row * CELL_SIZE + CELL_SIZE - CROSS_SPACE
                    
                    pygame.draw.line(screen, CROSS_COLOR,
                                   (x_start, y_start),
                                   (x_end, y_end),
                                   CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR,
                                   (x_start, y_end),
                                   (x_end, y_start),
                                   CROSS_WIDTH)

    def draw_player_info(self):
        # Draw current player info
        current_color = PLAYER_O_COLOR if self.current_player == 'O' else PLAYER_X_COLOR
        text = f"Current Player: {self.current_player}"
        text_surface = info_font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(topleft=(20, 10))
        pygame.draw.rect(screen, current_color, text_rect.inflate(20, 10))
        screen.blit(text_surface, text_rect)

    def make_move(self, row, col):
        if self.board[row][col] == '':
            self.board[row][col] = self.current_player
            # Set box color based on player
            self.box_colors[row][col] = PLAYER_O_COLOR if self.current_player == 'O' else PLAYER_X_COLOR
            self.current_player = 'X' if self.current_player == 'O' else 'O'
            return True
        return False

    def draw_board(self):
        # Draw background boxes with colors
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, 
                                 CELL_SIZE, CELL_SIZE)
                color = self.box_colors[row][col]
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)  # Box border

                if (row, col) == self.hover_cell and self.board[row][col] == '':
                    pygame.draw.rect(screen, HOVER_COLOR, rect)

        self.draw_lines()
        self.draw_symbols()
        self.draw_player_info()

    def check_winner(self):
        # Check rows
        for row in range(BOARD_SIZE):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                return self.board[row][0]

        # Check columns
        for col in range(BOARD_SIZE):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]

        # Check for draw
        if all(self.board[i][j] != '' for i in range(BOARD_SIZE) 
               for j in range(BOARD_SIZE)):
            return 'Draw'

        return None

    def draw_game_over(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 200))
        screen.blit(overlay, (0, 0))

        # Draw winner message
        if self.winner == 'Draw':
            text = "Game Over - It's a Tie!"
            color = TEXT_COLOR
        else:
            text = f"Player {self.winner} Wins!"
            color = CIRCLE_COLOR if self.winner == 'O' else CROSS_COLOR

        # Draw main message
        text_surface = game_font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 - 40))
        screen.blit(text_surface, text_rect)

        # Draw "Play Again?" message
        play_again_text = info_font.render("Click anywhere to play again", True, TEXT_COLOR)
        play_again_rect = play_again_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 + 40))
        screen.blit(play_again_text, play_again_rect)

    def reset_game(self):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'O'
        self.winner = None
        self.game_state = "playing"
        self.box_colors = [[EMPTY_BOX_COLOR for _ in range(BOARD_SIZE)] 
                          for _ in range(BOARD_SIZE)]

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()
            self.hover_cell = (int(mouse_pos[1] // CELL_SIZE), 
                             int(mouse_pos[0] // CELL_SIZE))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if self.game_state == "playing":
                        if self.winner is None:
                            row, col = self.hover_cell
                            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                                if self.make_move(row, col):
                                    self.winner = self.check_winner()
                                    if self.winner is not None:
                                        self.game_state = "game_over"
                    elif self.game_state == "game_over":
                        self.reset_game()

            screen.fill(BG_COLOR)
            self.draw_board()
            if self.game_state == "game_over":
                self.draw_game_over()

            pygame.display.flip()

if __name__ == '__main__':
    game = TicTacToe()
    game.run()