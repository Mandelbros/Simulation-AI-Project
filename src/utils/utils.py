

class Position:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

class Place:
    def __init__(self, id, position: Position) -> None:
        self.id = id
        self.position = position