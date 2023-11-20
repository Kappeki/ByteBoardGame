from Token import Token
from math import sqrt
import colors


class Board:

    def __init__(self, board_size, tile_size):
        self.board = {}
        self.board_size = board_size
        self.tile_size = tile_size
        self.playable_tiles = []
        self.board_light = colors.BEIGE
        self.board_dark = colors.BROWN
        self.clicked_token = None

    def initialize_board(self):
        self.board = {
            (row, column): [] if row in (0, self.board_size - 1) else [Token(row, column, row % 2)]
            for row in range(self.board_size)
            for column in range(self.board_size)
            if (row % 2 == column % 2)
        }
        self.playable_tiles = list(self.board.keys())

    def highlight_clicked_token(self, x, y):
        token_width = int(self.tile_size * 0.8)
        token_height = self.tile_size // 8
        tile_padding = (self.tile_size - token_width) / 2

        for stack in self.board.values():
            for token in stack:
                token_x, token_y = token.column*self.tile_size+tile_padding, (token.row+1)*self.tile_size-token_height*(token.level)

                token_x_min = token_x
                token_x_max = token_x + token_width
                token_y_min = token_y 
                token_y_max = token_y + token_height

                if token_x_min <= x <= token_x_max and token_y_min <= y <= token_y_max:
                    if self.clicked_token is None or self.clicked_token != token:
                        if self.clicked_token is not None:
                            self.clicked_token.clicked = False
                        token.clicked = True
                        self.clicked_token = token
                    else:
                        token.clicked = not token.clicked
                        if not token.clicked:
                            self.clicked_token = None

