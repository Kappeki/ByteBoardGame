import random
from color import fcolors


def get_clicked_tile_position(x, y, board_size, tile_size):
    row, column = [
        (row, column)
        for row in range(board_size)
        for column in range(board_size)
        if column*tile_size <= x <= (column+1)*tile_size and row*tile_size <= y <= (row+1)*tile_size
    ][0]
    return row, column

def are_neighbours(source_tile, destination_tile):
    x_distance = abs(destination_tile[1] - source_tile[1])
    y_distance = abs(destination_tile[0] - source_tile[0])
    if x_distance > 1 or y_distance > 1:
        return False
    return True

def add_tuples(tuple1, tuple2):
    return tuple(a + b for a, b in zip(tuple1, tuple2))

def can_move(board, destination_row, destination_column):
    """
    For now, this function is used to check which tiles to highlight as potential destinations
    In the furure, this function can be used for all movement constrain checks when moving a stack
    """
    selected_row = board.selected_tokens[0].row
    selected_column = board.selected_tokens[0].column

    # Checking token level
    lowest_selected_token_level = board.selected_tokens[0].level if board.selected_tokens else 0
    destination_highest_token_level = board.board[(destination_row, destination_column)][-1].level if board.board[(destination_row, destination_column)] else 0
    if lowest_selected_token_level >= destination_highest_token_level + 1:
        return False

    return True

def find_closest_directions(board_dict, current_row, current_col):
    closest_distance = float('inf')
    closest_tiles = []

    for (row, col), stack in board_dict.items():
        if stack and (row, col) != (current_row, current_col):
            distance = max(abs(row - current_row), abs(col - current_col))
            if distance < closest_distance:
                closest_distance = distance
                closest_tiles = [(row, col)]

    if not closest_tiles:
        return None
    
    for (row, col), stack in board_dict.items():
        if stack and (row, col) != (current_row, current_col) and (row, col) != closest_tiles[0]:
            distance = max(abs(row - current_row), abs(col - current_col))
            if distance == closest_distance:
                closest_tiles.append((row, col))

    possible_moves = set()

    for tile in closest_tiles:
        direction_row = tile[0] - current_row
        direction_col = tile[1] - current_col

        row_step = 1 if direction_row > 0 else (-1 if direction_row < 0 else 0)
        col_step = 1 if direction_col > 0 else (-1 if direction_col < 0 else 0)

        if abs(direction_row) > abs(direction_col):
            possible_moves.add((row_step, -1))
            possible_moves.add((row_step, 1))
        elif abs(direction_row) < abs(direction_col):
            possible_moves.add((-1, col_step))
            possible_moves.add((1, col_step))
        else:
            possible_moves.add((row_step, col_step))

    return list(possible_moves)

def has_neighbours(board_dict, board_size, selected_row, selected_column):
    if selected_row >= 1 and selected_column >= 1 and board_dict[(selected_row - 1, selected_column - 1)]:
        return True
    if selected_row >= 1 and selected_column < board_size-1 and board_dict[(selected_row - 1, selected_column + 1)]:
        return True
    if selected_row < board_size-1 and selected_column >= 1 and board_dict[(selected_row + 1, selected_column - 1)]:
        return True
    if selected_row < board_size-1 and selected_column < board_size-1 and board_dict[(selected_row + 1, selected_column + 1)]:
        return True
    return False

def determine_tile_color(board, row, column):
    selected_tile_row = board.selected_tokens[0].row if board.selected_tokens else -2
    selected_tile_column = board.selected_tokens[0].column if board.selected_tokens else -2
    highlighted_color = add_tuples(board.board_dark, (20, 20, 20))

    color = board.board_dark if (row + column) % 2 == 0 else board.board_light

    if (row + column) % 2 == 0 and board.selected_tokens:
        is_selected_tile = (selected_tile_row, selected_tile_column) == (row, column)
        is_neighbour = are_neighbours((selected_tile_row, selected_tile_column), (row, column))
        has_move = can_move(board, row, column)

        if has_neighbours(board.board, board.board_size, selected_tile_row, selected_tile_column):
            if not is_selected_tile and is_neighbour and has_move:
                color = highlighted_color
        else:
            if is_neighbour:
                potential_moves = [
                    add_tuples((selected_tile_row, selected_tile_column), direction)
                    for direction 
                    in find_closest_directions(board.board, selected_tile_row, selected_tile_column)
                ]
                if (row, column) in potential_moves:
                    color = highlighted_color

    return color

def print_score(human_points, computer_points):
    print(f'{fcolors.OKGREEN}############################')
    print(f'### Human: {human_points} Computer: {computer_points} ###')
    print(f'############################{fcolors.ENDC}')

def print_error(text):
    print(f'{fcolors.FAIL}{text}{fcolors.ENDC}')

def print_warning(text):
    print(f'{fcolors.WARNING}{text}{fcolors.ENDC}')

def print_green(text):
    print(f'{fcolors.OKGREEN}{text}{fcolors.ENDC}')