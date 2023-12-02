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
    selected_row = board.selected_tokens[0].row
    selected_column = board.selected_tokens[0].column

    lowest_selected_token_level = board.selected_tokens[0].level if board.selected_tokens else 0
    destination_highest_token_level = board.board[(destination_row, destination_column)][-1].level if board.board[(destination_row, destination_column)] else 0

    # Check for level constraint
    if lowest_selected_token_level >= destination_highest_token_level + 1:
        return False

    return True