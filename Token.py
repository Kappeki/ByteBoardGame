import colors


class Token:
    id = 0

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.level = 1
        self.color = colors.BLACK if color == 0 else colors.WHITE
        self.clicked = False
        self.border_thickness = 1
        self.id = Token.id

        Token.id += 1