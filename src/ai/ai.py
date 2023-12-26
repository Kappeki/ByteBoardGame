from typing import List, Dict, Tuple
import copy

from utils.movement import get_potential_moves, has_neighbours, is_inside_board

class AI:

    def __init__(
        self
    ) -> None:
        pass

    def get_next_positions(
        self, 
        board,
        player_color: Tuple[int, int, int]
    ) -> List[Dict]:
        potential_positions = []

        for position, stack in board.board.items():
            if not stack:
                continue
            tile_has_neighbours = has_neighbours(board.board, board.board_size, position[0], position[1])
            neighbour_tiles = [
                        (position[0]-1, position[1]-1),
                        (position[0]-1, position[1]+1),
                        (position[0]+1, position[1]+1),
                        (position[0]+1, position[1]-1)
                    ]

            for token in stack:
                # Has no neighbours
                if token.level == 1 and token.color == player_color and (not tile_has_neighbours):
                    # izvuci potencijalne poteze i dodaj ih u listu
                    potential_moves = get_potential_moves(board.board, board.board_size, position[0], position[1])
                    for potential_tile in potential_moves:
                        if not is_inside_board(potential_tile, board.board_size):
                            continue
                        new_board = self.ai_move_stack(board.board, position, token.level, potential_tile)
                        potential_positions.append(new_board)
                # Has neighbours
                if token.color == player_color and tile_has_neighbours:
                    for neighbour_tile in neighbour_tiles:
                        if not is_inside_board(neighbour_tile, board.board_size):
                            continue
                        neighbour_stack = board.board[neighbour_tile]
                        if neighbour_stack and board.is_destination_level_higher_than_current_level(token, neighbour_stack):
                            new_board = self.ai_move_stack(board.board, position, token.level, neighbour_tile)
                            potential_positions.append(new_board)
        return potential_positions

    def ai_move_stack(self, board_dict, source_tile, source_token_level, destination_tile):
        new_board = copy.deepcopy(board_dict)
        token_index = source_token_level - 1
        destination_max_index = len(new_board[destination_tile]) - 1

        tokens = new_board[source_tile][token_index:]
        for token in tokens:
            token.move(destination_tile[0], destination_tile[1], destination_max_index+1)
            destination_max_index += 1

        new_board[destination_tile] = new_board[source_tile][token_index:]
        new_board[source_tile] = new_board[source_tile][:token_index]

        return new_board