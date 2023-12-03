import pygame
import color.colors as colors
from Board import Board
from Token import Token
from utils import add_tuples, determine_tile_color


class GUI:

    def __init__(self, screen):
        self.screen = screen

    def draw_board(self, board: Board):
        # Define whose turn it is
        if board.current_player in ['h', 'H']:
            pygame.display.set_caption('Byte - HUMAN TURN (white)')
        else:
            pygame.display.set_caption('Byte - COMPUTER TURN (black) ')

        # Draw board
        for row in range(board.board_size):
            for column in range(board.board_size):
                
                color = determine_tile_color(board, row, column)
                tile_rect = (column*board.tile_size, row*board.tile_size, board.tile_size, board.tile_size)
                pygame.draw.rect(self.screen, color, tile_rect)

                if (row, column) in board.playable_tiles:
                    stack = board.board[(row, column)]
                    self.draw_stack(stack, board.tile_size)

    def draw_stack(self, stack, tile_size):
        for token in stack:
            self.draw_token(token, tile_size)

    def draw_token(self, token: Token, tile_size):
        tile_padding = (tile_size - token.width) / 2
        token_color = token.color
        token_size = (token.width, token.height)
        token_thickness = 3 if token.selected else token.border_thickness
        token_position_x = token.column*tile_size + tile_padding
        token_position_y = (token.row+1)*tile_size - token.height*(token.level)
        token_position = (token_position_x, token_position_y)

        border_rect = [
            token_position[0] - token_thickness,
            token_position[1] - token_thickness,
            token_size[0] + token_thickness * 2,
            token_size[1] + token_thickness * 2
        ]
        border_color = colors.GREEN if token.selected else colors.BLACK if token_color == colors.WHITE else colors.WHITE

        pygame.draw.rect(self.screen, border_color, border_rect)    
        pygame.draw.rect(self.screen, token_color, (token_position, token_size))

