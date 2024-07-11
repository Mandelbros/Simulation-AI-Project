class Position:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.row == other.row and self.col == other.col
        return False

    def __hash__(self):
        return hash((self.row, self.col))
        
    def __str__(self):
        return f"({self.row}, {self.col})"
    
    def __repr__(self):
        return f"({self.row}, {self.col})"
    
class Place:
    def __init__(self, id, position: Position) -> None:
        self.id = id
        self.position = position

    def __eq__(self, other):
        if isinstance(other, Place):
            return self.id == other.id and self.position == other.position
        return False
    
    def __str__(self):
        return f"Place(id={self.id}, position={self.position})"
    
    def __repr__(self):
        return f"Place(id={self.id}, position={self.position})"