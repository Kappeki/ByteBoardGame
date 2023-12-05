from typing import List, Literal, Dict, Tuple

from .token import Token
from utils import colors
from utils.movement import get_clicked_tile_position, are_neighbours
from utils.utils import print_error, print_green, print_score, print_warning


class Board:

    def __init__(
            self, 
            board_size: int, 
            tile_size: int, 
            current_player: Literal['h', 'H', 'c', 'C']
        ) -> None:
        self.board: Dict = {}
        self.human_points: int = 0
        self.computer_points: int = 0
        self.tile_size: int = tile_size
        self.board_size: int = board_size
        self.selected_tokens: List[Token] = []
        self.board_dark: Tuple[int, int, int] = colors.BROWN
        self.board_light: Tuple[int, int, int] = colors.BEIGE
        self.current_player: Literal['h', 'H', 'c', 'C'] = current_player

    def change_selected_tokens_status(
            self
        ) -> None:
        [selected_token.change_selected_status() for selected_token in self.selected_tokens]

    def initialize_board(
            self
        ) -> None:
        token_width = int(self.tile_size * 0.8)
        token_height = self.tile_size // 8
        self.board = {
            (row, column): [] if row in (0, self.board_size - 1) else [
                Token(row, column, colors.BLACK if row % 2 else colors.WHITE, token_width, token_height, 1),
                # Token(row, column, row % 2, token_width, token_height, 2),
                # Token(row, column, row % 2, token_width, token_height, 3),
            ]
            for row in range(self.board_size)
            for column in range(self.board_size)
            if (row % 2 == column % 2)
        }

    def highlight_clicked_token(
            self, 
            x: int, 
            y: int
        ) -> None:
        token_width = int(self.tile_size * 0.8)
        token_height = self.tile_size // 8
        tile_padding = (self.tile_size - token_width) / 2
        row, column = get_clicked_tile_position(x, y, self.tile_size)

        if (row, column) in self.board:
            stack = self.board[(row, column)]
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
                    # Deselect token
                    if self.selected_tokens and token == self.selected_tokens[0]:
                        self.change_selected_tokens_status()
                        self.selected_tokens = []
                        return
                    self.change_selected_tokens_status()
                    self.selected_tokens = []
                    self.selected_tokens = [stack[j] for j in range(i, len(stack))]
                    self.change_selected_tokens_status()


    def move_stack(
            self, 
            row: int, 
            column: int
        ) -> bool:

        is_winning_move = False

        # Check if token was selected
        selected_tokens_count = len(self.selected_tokens)
        if selected_tokens_count == 0:
            print_warning("No token was selected")
            return is_winning_move

        # Check if row, column are playable tiles
        if (row, column) not in self.board:
            print_error("Tile is not playable")
            return is_winning_move
        
        current_row = self.selected_tokens[0].row
        current_column = self.selected_tokens[0].column

        # Check if destination tile is the same as current tile
        if row == current_row and column == current_column:
            print_warning("Source and destination tiles are same")
            return is_winning_move
        
        # Check if tiles are in neighbourhood
        if not are_neighbours((current_row, current_column), (row, column)):
            print_error("Destination tile is too far away")
            return is_winning_move
        
        current_tile_tokens_count = len(self.board[(current_row, current_column)])
        destination_tile_tokens_count = len(self.board[(row, column)])

        # Check if resulting level is higher than the starting level
        if self.selected_tokens[0].level >= destination_tile_tokens_count + 1:
            print_error("You are attempting to move token to lower or equal level")
            return is_winning_move
        
        # Check if resulting stack would have more than 8 tokens
        resulting_stack_size = selected_tokens_count + destination_tile_tokens_count
        if resulting_stack_size > 8:
            print_error(f"You are attempting to make stack of size {resulting_stack_size}")
            return is_winning_move

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
            print_green("Stack with size 8 was created")
            # Delete the tokens
            self.board[(row, column)] = []
            # Update the points
            if self.current_player in ['h', 'H']:
                self.human_points += 1
            else:
                self.computer_points += 1
            # Check if there is a winner
            max_points = (self.board_size**2 - 2*self.board_size) // 16
            winning_point = max_points // 2 + 1
            if self.human_points == winning_point or self.computer_points == winning_point:
                is_winning_move = True
            else:
                print_score(self.human_points, self.computer_points)
            
        # Change current player
        self.current_player = 'h' if self.current_player in ['c', 'C'] else 'c'

        return is_winning_move
