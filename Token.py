import colors


class Token:
    id = 0

    def __init__(self, row, column, color, width, height, level=1):
        self.row = row
        self.column = column
        self.level = level
        self.color = colors.BLACK if color == 0 else colors.WHITE
        self.width = width
        self.height = height
        self.selected = False
        self.border_thickness = 1
        self.id = Token.id

        Token.id += 1

    def change_selected_status(self, status=None):
        if status is None:
            self.selected = not self.selected
        else:
            self.selected = status

    def move(self, dest_row, dest_column, dest_level):
        self.row = dest_row
        self.column = dest_column
        self.level = dest_level

    def __repr__(self):
        return f'id:{self.id};row:{self.row};column:{self.column};level:{self.level}'
