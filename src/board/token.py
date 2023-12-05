from typing import Tuple, Union


class Token:
    id = 0

    def __init__( 
            self, 
            row: int, 
            column: int, 
            color: Tuple[int, int, int], 
            width: int, 
            height: int, 
            level: int = 1
        ) -> None:
        self.row = row
        self.column = column
        self.level = level
        self.color = color
        self.width = width
        self.height = height
        self.selected = False
        self.border_thickness = 1
        self.id = Token.id

        Token.id += 1

    def change_selected_status(
            self, 
            status: Union[bool, None]=None
        ) -> None:
        if status is None:
            self.selected = not self.selected
        else:
            self.selected = status

    def move(
            self,
            dest_row: int, 
            dest_column: int, 
            dest_level: int
        ) -> None:
        self.row = dest_row
        self.column = dest_column
        self.level = dest_level

    def __repr__(
            self
        ) -> str:
        return f'id:{self.id};row:{self.row};column:{self.column};level:{self.level}'
