import pygame
from typing import List, Literal, Tuple

from utils import colors
from board.board import Board
from board.token import Token


class GUI:

    def __init__(
            self, 
            screen: pygame.Surface
        ) -> None:
        self.screen = screen

    def draw_board(
            self, 
            board: Board
        ) -> None:
        for row in range(board.board_size):
            for column in range(board.board_size):

                color = board.determine_tile_color(row, column)
                tile_rect = (column*board.tile_size, row*board.tile_size, board.tile_size, board.tile_size)
                pygame.draw.rect(self.screen, color, tile_rect)

                if (row, column) in board.board:
                    stack = board.board[(row, column)]
                    self.draw_stack(stack, board.tile_size)

    def draw_stack(
            self, 
            stack: List[Token], 
            tile_size: int
        ) -> None:
        for token in stack:
            self.draw_token(token, tile_size)

    def draw_token(
            self, 
            token: Token, 
            tile_size: int
        ) -> None:
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
        border_color = self.get_border_color(token)

        pygame.draw.rect(self.screen, border_color, border_rect)    
        pygame.draw.rect(self.screen, token_color, (token_position, token_size))

    def get_border_color(
            self, 
            token: Token
        ) -> Tuple[int, int, int]:
        if token.selected:
            return colors.GREEN
        elif token.color == colors.WHITE:
            return colors.BLACK
        else:
            return colors.WHITE

    def update_caption(
            self, 
            current_player: Literal['h', 'H', 'c', 'C']
        ) -> None:
        if current_player in ['h', 'H']:
            pygame.display.set_caption('Byte - HUMAN TURN (white)')
        else:
            pygame.display.set_caption('Byte - COMPUTER TURN (black)')