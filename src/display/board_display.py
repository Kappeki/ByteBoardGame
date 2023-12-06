from utils.movement import are_neighbours, can_move, get_potential_moves, has_neighbours


def determine_tile_color(board, row, column):
    base_color = get_base_tile_color(board, row, column)
    if should_highlight_tile(board, row, column):
        return lighten_color(base_color)
    return base_color

def get_base_tile_color(board, row, column):
    if (row + column) % 2 == 0:
        return board.board_dark
    else:
        return board.board_light

def should_highlight_tile(board, row, column):
    if not board.selected_tokens:
        return False

    selected_tile_row, selected_tile_column = get_selected_tile_position(board)
    is_neighbour = are_neighbours((selected_tile_row, selected_tile_column), (row, column))
    has_move = can_move(board, row, column)

    if has_neighbours(board.board, board.board_size, selected_tile_row, selected_tile_column):
        return not is_selected_tile(selected_tile_row, selected_tile_column, row, column) and is_neighbour and has_move
    else:
        potential_moves = get_potential_moves(board.board, board.board_size, selected_tile_row, selected_tile_column)
        return (row, column) in potential_moves

def lighten_color(color):
    return tuple(min(c + 20, 255) for c in color)

def get_selected_tile_position(board):
    return board.selected_tokens[0].row, board.selected_tokens[0].column

def is_selected_tile(selected_row, selected_col, row, column):
    return (selected_row, selected_col) == (row, column)