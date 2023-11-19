import pygame
from colors import *

class GUI:

    def __init__(self, screen, grid_size):
        self.screen = screen
        self.grid_size = grid_size
        self.tile_size = screen.get_height() // self.grid_size
        self.token_width = int(self.tile_size * 0.8)
        self.token_height = self.tile_size // 8
        self.board_white = BOARD_WHITE
        self.board_black = BOARD_BLACK
        self.token_white = TOKEN_WHITE
        self.token_black = TOKEN_BLACK

    def draw_board(self, board):
        playable_tiles = list(board.keys())

        for row in range(self.grid_size):
            for column in range(self.grid_size):

                color = self.board_black if (row + column) % 2 == 0 else self.board_white
                pygame.draw.rect(self.screen, color, (column*self.tile_size, row*self.tile_size, self.tile_size, self.tile_size))

                if (row, column) in playable_tiles:
                    stack = board[(row, column)]
                    self.draw_stack(stack, row, column)

    def draw_stack(self, stack, row, column):
        token_size = (self.token_width, self.token_height)
        tile_padding = (self.tile_size - self.token_width) / 2
        for i in range(len(stack)):
            token_position = (column*self.tile_size+tile_padding, (row+1)*self.tile_size-self.token_height*(i+1))
            self.draw_token(stack[i], token_position, token_size, 1)


    def draw_token(self, color, position, size, border_thickness):
        border_rect = [
            position[0] - border_thickness,
            position[1] - border_thickness,
            size[0] + border_thickness * 2,
            size[1] + border_thickness * 2
        ]
        token_color = self.token_black if color == 0 else self.token_white
        border_color = self.token_white if color == 0 else self.token_black
        pygame.draw.rect(self.screen, border_color, border_rect)    
        pygame.draw.rect(self.screen, token_color, (position, size))

