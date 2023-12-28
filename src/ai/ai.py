from typing import List, Dict, Tuple
import copy

import utils.colors as colors
from board.token import Token
from utils.utils import final_stack
from utils.movement import get_potential_moves, has_neighbours, is_destination_level_higher_than_current_level, is_inside_board


class AI:

    def __init__(
            self
        ) -> None:
        pass

    def ai_get_next_positions(
            self,
            board_dict,
            board_size,
            player_color: Tuple[int, int, int]
        ) -> List[Dict]:
        potential_positions = []

        for tile, stack in board_dict.items():
            if not stack:
                continue
            tile_has_neighbours = has_neighbours(board_dict, board_size, tile[0], tile[1])
            neighbour_tiles = [
                        (tile[0]-1, tile[1]-1),
                        (tile[0]-1, tile[1]+1),
                        (tile[0]+1, tile[1]+1),
                        (tile[0]+1, tile[1]-1)
                    ]

            for token in stack:
                # Has no neighbours
                if token.level == 1 and token.color == player_color and (not tile_has_neighbours):
                    potential_moves = get_potential_moves(board_dict, board_size, tile[0], tile[1])
                    for potential_tile in potential_moves:
                        if not is_inside_board(potential_tile, board_size):
                            continue
                        new_board = self.ai_move_stack(board_dict, tile, token.level, potential_tile)
                        potential_positions.append(new_board)
                # Has neighbours
                if token.color == player_color and tile_has_neighbours:
                    for neighbour_tile in neighbour_tiles:
                        # Check if neighbour tile is inside the board
                        if not is_inside_board(neighbour_tile, board_size):
                            continue
                        neighbour_stack = board_dict[neighbour_tile]
                        # Check if token would have higher level if moved to destination stack
                        if not neighbour_stack or not is_destination_level_higher_than_current_level(token, neighbour_stack):
                            continue
                        # Check if resulting stack would have more than 8 tokens
                        if len(neighbour_stack) + len(stack) - (token.level - 1) > 8:
                            continue
                        new_board = self.ai_move_stack(board_dict, tile, token.level, neighbour_tile)
                        potential_positions.append(new_board)

        return potential_positions

    def ai_move_stack(
            self, 
            board_dict, 
            source_tile: Tuple[int, int], 
            source_token_level: int, 
            destination_tile: Tuple[int, int]
        ) -> Dict[Tuple[int, int], List[Token]]:
        new_board = copy.deepcopy(board_dict)
        source_token_index = source_token_level - 1
        destination_max_level = len(new_board[destination_tile])

        selected_tokens = new_board[source_tile][source_token_index:]
        for token in selected_tokens:
            token.move(destination_tile[0], destination_tile[1], destination_max_level+1)
            destination_max_level += 1

        new_board[destination_tile] = [*new_board[destination_tile], *selected_tokens]
        new_board[source_tile] = new_board[source_tile][:source_token_index]

        return new_board
    
    def ai_make_move(
            self, 
            board_dict,
            board_size,
            current_player_color
        ) -> None:

        is_maximizing_player = current_player_color == colors.WHITE
        print('Starting minimax algorithm...')
        # board_dict = {
        #     (0,0): [],
        #     (0,2): [],
        #     (0,4): [],
        #     (0,6): [],
        #     (1,1): [],
        #     (1,3): [
        #         Token(1,3,colors.BLACK, 80, 20, 1),
        #         Token(1,3,colors.WHITE, 80, 20, 2),
        #         Token(1,3,colors.BLACK, 80, 20, 3),
        #         Token(1,3,colors.WHITE, 80, 20, 4),
        #         Token(1,3,colors.WHITE, 80, 20, 5),
        #         ],
        #     (1,5): [],
        #     (1,7): [],

        #     (2,0): [],
        #     (2,2): [],
        #     (2,4): [],
        #     (2,6): [],
        #     (3,1): [],
        #     (3,3): [],
        #     (3,5): [],
        #     (3,7): [],

        #     (4,0): [],
        #     (4,2): [],
        #     (4,4): [],
        #     (4,6): [Token(4,6,colors.BLACK, 80, 20, 1)],
        #     (5,1): [],
        #     (5,3): [],
        #     (5,5): [],
        #     (5,7): [
        #         Token(5,7,colors.WHITE, 80, 20, 1),
        #         Token(5,7,colors.BLACK, 80, 20, 2),
        #     ],

        #     (6,0): [],
        #     (6,2): [],
        #     (6,4): [],
        #     (6,6): [],
        #     (7,1): [],
        #     (7,3): [],
        #     (7,5): [],
        #     (7,7): [],
        # }
        best_heuristic_value, best_move = self.minimax(board_dict, board_size, 3, is_maximizing_player)
        print(f'Best heuristic value found for this position: {best_heuristic_value}')

        return best_move

    # Plain minimax algorithm
    # def minimax(
    #         self, 
    #         board_dict,
    #         board_size,
    #         depth,
    #         is_maximizing_player
    #     ) -> Tuple[int, Dict[Tuple[int, int], List[Token]]]:
    #     if depth == 0 or final_stack(board_dict):
    #         return self.heuristic(board_dict, board_size), None

    #     # Determine the color of the opponent based on the current player color
    #     player_color = colors.WHITE if is_maximizing_player else colors.BLACK
    #     best_move = board_dict
    #     next_positions = self.ai_get_next_positions(board_dict, board_size, player_color)

    #     if len(next_positions) == 0:
    #         return 0, None

    #     if is_maximizing_player:
    #         best_value = float('-inf')
    #         for new_board in next_positions:
    #             heuristic_value, _ = self.minimax(new_board, board_size, depth - 1, False)

    #             if heuristic_value > best_value:
    #                 best_value = heuristic_value
    #                 best_move = new_board

    #         return best_value, best_move
        
    #     else:
    #         best_value = float('inf')
    #         for new_board in next_positions:
    #             heuristic_value, _ = self.minimax(new_board, board_size, depth - 1, True)
    #             if heuristic_value < best_value:
    #                 best_value = heuristic_value
    #                 best_move = new_board

    #         return best_value, best_move

    def minimax(
            self, 
            board_dict,
            board_size,
            depth,
            is_maximizing_player,
            alpha=float('-inf'), 
            beta=float('inf')
        ) -> Tuple[int, Dict[Tuple[int, int], List[Token]]]:
        if depth == 0 or final_stack(board_dict):
            return self.heuristic(board_dict, board_size), board_dict

        player_color = colors.WHITE if is_maximizing_player else colors.BLACK
        best_move = board_dict
        next_positions = self.ai_get_next_positions(board_dict, board_size, player_color)

        if len(next_positions) == 0:
            return self.heuristic(board_dict, board_size), board_dict

        if is_maximizing_player:
            best_value = float('-inf')
            for new_board in next_positions:
                heuristic_value, _ = self.minimax(new_board, board_size, depth - 1, False, alpha, beta)

                if heuristic_value > best_value:
                    best_value = heuristic_value
                    best_move = new_board

                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            return best_value, best_move
        
        else:
            best_value = float('inf')
            for new_board in next_positions:
                heuristic_value, _ = self.minimax(new_board, board_size, depth - 1, True, alpha, beta)

                if heuristic_value < best_value:
                    best_value = heuristic_value
                    best_move = new_board

                beta = min(beta, best_value)
                if beta <= alpha:
                    break

            return best_value, best_move

    def heuristic(
            self, 
            board_dict,
            board_size
        ):
        score = 0

        for tile, stack in board_dict.items():
            if not stack:
                continue

            # Stack Height Value
            stack_height = len(stack)
            stack_height_score = 2 ** (stack_height - 1)
            stack_height_score = stack_height_score if stack[-1].color == colors.WHITE else -stack_height_score

            # Mobility Score
            mobility = len(get_potential_moves(board_dict, board_size, tile[0], tile[1]))
            mobility_score = mobility * 2
            mobility_score = mobility_score if stack[-1].color == colors.WHITE else -mobility_score

            # Control of Center
            center_control_score = 0
            if self.is_center(tile, board_size):
                center_control_score = 5 if stack[-1].color == colors.WHITE else -5

            # Check for 8-token stack and add 50 points to the owner
            eight_token_stack_score = 0
            if stack_height == 8:
                eight_token_stack_score = 50 if stack[-1].color == colors.WHITE else -50                

            score += stack_height_score + mobility_score + center_control_score + eight_token_stack_score
        
        return score

    def is_center(self, tile, board_size):
        center_area = range(board_size // 4, 3 * board_size // 4)
        return tile[0] in center_area and tile[1] in center_area