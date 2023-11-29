from Token import Token
import color.colors as colors
import color.fcolors as fcolors
from typing import List
from utils import are_neighbours


class Board:

    def __init__(self, board_size, tile_size, current_player):
        self.board = {}
        self.board_size = board_size
        self.tile_size = tile_size
        self.playable_tiles = []
        self.board_light = colors.BEIGE
        self.board_dark = colors.BROWN
        self.selected_tokens: List[Token] = []
        self.current_player = current_player

    def change_selected_tokens_status(self):
        [selected_token.change_selected_status() for selected_token in self.selected_tokens]

    def initialize_board(self):
        token_width = int(self.tile_size * 0.8)
        token_height = self.tile_size // 8
        self.board = {
            (row, column): [] if row in (0, self.board_size - 1) else [
                Token(row, column, row % 2, token_width, token_height, 1),
                # Token(row, column, row % 2, token_width, token_height, 2),
                # Token(row, column, row % 2, token_width, token_height, 3),
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
                token_x = token.column * self.tile_size + tile_padding
                token_y = (token.row+1) * self.tile_size - token_height * token.level

                token_x_min = token_x
                token_x_max = token_x + token_width
                token_y_min = token_y 
                token_y_max = token_y + token_height

                if token_x_min <= x <= token_x_max and token_y_min <= y <= token_y_max:
                    # Abort if opposite player token has been attempted to select
                    if self.current_player in ['h', 'H'] and token.color == colors.BLACK:
                        return
                    if self.current_player in ['c', 'C'] and token.color == colors.WHITE:
                        return
                    
                    if self.selected_tokens and token == self.selected_tokens[0]:
                        self.change_selected_tokens_status()
                        self.selected_tokens = []
                        return
                    self.change_selected_tokens_status()
                    self.selected_tokens = []
                    self.selected_tokens = [stack[j] for j in range(i, len(stack))]
                    self.change_selected_tokens_status()

    def move_stack(self, row, column):
        # Check if token was selected
        selected_tokens_count = len(self.selected_tokens)
        if selected_tokens_count == 0:
            print(f'{fcolors.WARNING}No token was selected{fcolors.ENDC}')
            return

        # Check if row, column are playable tiles
        if (row, column) not in self.playable_tiles:
            print(f'{fcolors.FAIL}Tile is not playable{fcolors.ENDC}')
            return
        
        current_row = self.selected_tokens[0].row
        current_column = self.selected_tokens[0].column

        # Check if destination tile is the same as current tile
        if row == current_row and column == current_column:
            print(f'{fcolors.WARNING}Source and destination tiles are same{fcolors.ENDC}')
            return
        
        # Check if tiles are in neighbourhood
        if not are_neighbours((current_row, current_column), (row, column)):
            print(f'{fcolors.FAIL}Destination tile is too far away{fcolors.ENDC}')
            return
        
        current_tile_tokens_count = len(self.board[(current_row, current_column)])
        destination_tile_tokens_count = len(self.board[(row, column)])

        # Check if resulting level is higher than the starting level
        if self.selected_tokens[0].level >= destination_tile_tokens_count + 1:
            print(f'{fcolors.FAIL}You are attempting to move token to lower or equal level{fcolors.ENDC}')
            return
        
        # Check if resulting stack would have more than 8 tokens
        resulting_stack_size = selected_tokens_count + destination_tile_tokens_count
        if resulting_stack_size > 8:
            print(f'{fcolors.FAIL}You are attempting to make stack of size {resulting_stack_size}{fcolors.ENDC}')
            return

        # Update old tile in board dictionary
        self.board[(current_row, current_column)] = self.board[(current_row, current_column)][:current_tile_tokens_count-selected_tokens_count]
        
        # Update token objects
        for token in self.selected_tokens:
            token.move(row, column, destination_tile_tokens_count + 1)
            destination_tile_tokens_count += 1

        # Update new tile in board dictionary
        self.board[(row, column)] = [*self.board[(row, column)], *self.selected_tokens]

        # Deselect tokens
        self.change_selected_tokens_status()
        self.selected_tokens = []

        # Check if stack of size 8 has been created
        if len(self.board[(row, column)]) == 8:
            print(f'{fcolors.OKGREEN}Stack with size 8 was created{fcolors.ENDC}')
            # Delete the tokens
            self.board[(row, column)] = []

        # Change current player
        self.current_player = 'h' if self.current_player in ['c', 'C'] else 'c'

