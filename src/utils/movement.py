from .utils import add_tuples


def get_clicked_tile_position(x, y, tile_size):
    column = x // tile_size
    row = y // tile_size
    return row, column

def can_move(board, destination_row, destination_column):
    """
    For now, this function is used to check which tiles to highlight as potential destinations
    In the furure, this function can be used for all movement constrain checks when moving a stack
    """
    selected_row = board.selected_tokens[0].row
    selected_column = board.selected_tokens[0].column

    # Checking token level
    lowest_selected_token_level = board.selected_tokens[0].level if board.selected_tokens else 0
    destination_stack = board.board.get((destination_row, destination_column), [])
    highest_destination_token_level = destination_stack[-1].level if destination_stack else 0

    if lowest_selected_token_level >= highest_destination_token_level + 1:
        return False

    return True

def are_neighbours(source_tile, destination_tile):
    if source_tile == destination_tile:
        return False
    x_distance = abs(destination_tile[1] - source_tile[1])
    y_distance = abs(destination_tile[0] - source_tile[0])
    if x_distance > 1 or y_distance > 1:
        return False
    return True

def has_neighbours(board_dict, board_size, selected_row, selected_column):
    neighbor_positions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for row_offset, col_offset in neighbor_positions:
        neighbor_row = selected_row + row_offset
        neighbor_col = selected_column + col_offset
        
        if 0 <= neighbor_row < board_size and 0 <= neighbor_col < board_size:
            if board_dict.get((neighbor_row, neighbor_col)):
                return True

    return False

def find_closest_directions(board_dict, current_row, current_col, board_size):
    closest_distance = float('inf')
    closest_tiles = []

    for (row, col), stack in board_dict.items():
        if stack and (row, col) != (current_row, current_col):
            distance = max(abs(row - current_row), abs(col - current_col))
            if distance < closest_distance:
                closest_distance = distance
                closest_tiles = [(row, col)]
            elif distance == closest_distance:
                closest_tiles.append((row, col))

    if not closest_tiles:
        return closest_tiles
    
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

def get_potential_moves(board, selected_row, selected_column):
    closest_directions = find_closest_directions(board.board, selected_row, selected_column, board.board_size)

    # Filter for valid diagonal moves on black tiles
    potential_moves = [
        add_tuples((selected_row, selected_column), direction)
        for direction in closest_directions
        if is_black_tile(*add_tuples((selected_row, selected_column), direction))
    ]

    return potential_moves

def is_black_tile(row, column):
    return (row + column) % 2 == 0
