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
