import pygame
import colors
from Board import Board
from Token import Token


class GUI:

    def __init__(self, screen):
        self.screen = screen

    def draw_board(self, board: Board):
        for row in range(board.board_size):
            for column in range(board.board_size):

                color = board.board_dark if (row + column) % 2 == 0 else board.board_light
                pygame.draw.rect(self.screen, color, (column*board.tile_size, row*board.tile_size, board.tile_size, board.tile_size))

                if (row, column) in board.playable_tiles:
                    stack = board.board[(row, column)]
                    self.draw_stack(stack, board.tile_size)

    def draw_stack(self, stack, tile_size):
        for token in stack:
            self.draw_token(token, tile_size)

    def draw_token(self, token: Token, tile_size):
        token_row = token.row
        token_column = token.column
        token_level = token.level
        token_is_clicked = token.clicked
        token_color = token.color if not token_is_clicked else colors.GREEN
        token_width = int(tile_size * 0.8)
        token_height = tile_size // 8
        token_border_thickness = token.border_thickness

        tile_padding = (tile_size - token_width) / 2

        token_position = (token_column*tile_size+tile_padding, (token_row+1)*tile_size-token_height*(token_level))
        token_size = (token_width, token_height)

        border_rect = [
            token_position[0] - token_border_thickness,
            token_position[1] - token_border_thickness,
            token_size[0] + token_border_thickness * 2,
            token_size[1] + token_border_thickness * 2
        ]
        border_color = colors.WHITE if token_color == colors.BLACK else colors.BLACK
        pygame.draw.rect(self.screen, border_color, border_rect)    
        pygame.draw.rect(self.screen, token_color, (token_position, token_size))

