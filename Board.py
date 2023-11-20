from Token import Token
import colors
from typing import List

class Board:

    def __init__(self, board_size, tile_size):
        self.board = {}
        self.board_size = board_size
        self.tile_size = tile_size
        self.playable_tiles = []
        self.board_light = colors.BEIGE
        self.board_dark = colors.BROWN
        self.selected_tokens: List[Token] = []

    def change_selected_tokens_status(self):
        [selected_token.change_selected_status() for selected_token in self.selected_tokens]


    def initialize_board(self):
        token_width = int(self.tile_size * 0.8)
        token_height = self.tile_size // 8
        self.board = {
            (row, column): [] if row in (0, self.board_size - 1) else [
                Token(row, column, row % 2, token_width, token_height, 1),
                Token(row, column, row % 2, token_width, token_height, 2),
                Token(row, column, row % 2, token_width, token_height, 3),
            ]
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
            for i in range(len(stack)):
                token = stack[i]
                token_x = token.column*self.tile_size+tile_padding
                token_y = (token.row+1)*self.tile_size-token_height*(token.level)

                token_x_min = token_x
                token_x_max = token_x + token_width
                token_y_min = token_y 
                token_y_max = token_y + token_height

                if token_x_min <= x <= token_x_max and token_y_min <= y <= token_y_max:
                    if self.selected_tokens and token == self.selected_tokens[0]:
                        self.change_selected_tokens_status()
                        self.selected_tokens = []
                        return
                    self.change_selected_tokens_status()
                    self.selected_tokens = []
                    self.selected_tokens = [stack[j] for j in range(i, len(stack))]
                    self.change_selected_tokens_status()

    def get_clicked_tile_position(self, x, y):
        row, column = [
            (row, column)
            for row in range(self.board_size)
            for column in range(self.board_size)
            if column*self.tile_size <= x <= (column+1)*self.tile_size and row*self.tile_size <= y <= (row+1)*self.tile_size
        ][0]
        return row, column
    
    def move_stack(self, row, column):
        selected_tokens_count = len(self.selected_tokens)
        if selected_tokens_count == 0:
            return
        
        current_row = self.selected_tokens[0].row
        current_column = self.selected_tokens[0].column

        # Update old tile in board dictionary
        tile_tokens_count = len(self.board[(current_row, current_column)])
        self.board[(current_row, current_column)] = self.board[(current_row, current_column)][:tile_tokens_count-selected_tokens_count]
        
        # Update token objects
        destination_tile_level = len(self.board[(row, column)])
        for token in self.selected_tokens:
            token.level = destination_tile_level + 1
            destination_tile_level += 1
            token.row = row
            token.column = column

        # Update new tile in board dictionary
        self.board[(row, column)] = [*self.board[(row, column)], *self.selected_tokens]

        # Deselect tokens
        self.change_selected_tokens_status()
        self.selected_tokens = []

