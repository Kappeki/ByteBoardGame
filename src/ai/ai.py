from typing import List, Dict, Tuple
import copy

from utils.movement import get_potential_moves, has_neighbours, is_inside_board
from board.token import Token

class AI:

    def __init__(
        self
    ) -> None:
        pass

    def ai_get_next_positions(
        self,
        board,
        player_color: Tuple[int, int, int]
    ) -> List[Dict]:
        potential_positions = []

        for tile, stack in board.board.items():
            if not stack:
                continue
            tile_has_neighbours = has_neighbours(board.board, board.board_size, tile[0], tile[1])
            neighbour_tiles = [
                        (tile[0]-1, tile[1]-1),
                        (tile[0]-1, tile[1]+1),
                        (tile[0]+1, tile[1]+1),
                        (tile[0]+1, tile[1]-1)
                    ]

            for token in stack:
                # Has no neighbours
                if token.level == 1 and token.color == player_color and (not tile_has_neighbours):
                    potential_moves = get_potential_moves(board.board, board.board_size, tile[0], tile[1])
                    for potential_tile in potential_moves:
                        if not is_inside_board(potential_tile, board.board_size):
                            continue
                        new_board = self.ai_move_stack(board, tile, token.level, potential_tile)
                        potential_positions.append(new_board)
                # Has neighbours
                if token.color == player_color and tile_has_neighbours:
                    for neighbour_tile in neighbour_tiles:
                        if not is_inside_board(neighbour_tile, board.board_size):
                            continue
                        neighbour_stack = board.board[neighbour_tile]
                        if neighbour_stack and board.is_destination_level_higher_than_current_level(token, neighbour_stack):
                            if len(neighbour_stack) + len(stack) - (token.level - 1) <= 8:
                                new_board = self.ai_move_stack(board, tile, token.level, neighbour_tile)
                                potential_positions.append(new_board)
        return potential_positions

    def ai_move_stack(self, board, source_tile, source_token_level, destination_tile) -> Dict[Tuple[int, int], List[Token]]:
        new_board = copy.deepcopy(board.board)
        token_index = source_token_level - 1
        destination_max_level = len(new_board[destination_tile])

        tokens = new_board[source_tile][token_index:]
        for token in tokens:
            token.move(destination_tile[0], destination_tile[1], destination_max_level+1)
            destination_max_level += 1

        new_board[destination_tile] = [*new_board[destination_tile], *new_board[source_tile][token_index:]]
        new_board[source_tile] = new_board[source_tile][:token_index]

        return new_board
    
    def ai_make_move(self, board, player_color: Tuple[int, int, int] ) -> None:
        next_positions = self.ai_get_next_positions(board, player_color)
        position = next_positions[0]
        board.board = position
    