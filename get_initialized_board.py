def get_initialized_board(N):
    board = {
        (row, column): [] if row in (0, N - 1) else [row % 2]
        for row in range(N)
        for column in range(N)
        if (row % 2 == column % 2)
    }
    return board