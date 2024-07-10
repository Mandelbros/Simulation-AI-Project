from src.utils.utils import Position, Place

class Table(Place):
    def __init__(self, id, position: Position, is_available):
        super.__init__(id, position)
        self.is_available = is_available