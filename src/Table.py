from src.utils.utils import Position, Place

class Table(Place):
    def __init__(self, id, position: Position):
        super.__init__(id, position)