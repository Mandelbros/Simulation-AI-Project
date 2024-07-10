from src.utils.utils import Position
from typing import List

class Agent():
    def __init__(self, id, position: Position = None):
        self.id = id
        self.position: Position = position
        self.cur_walk_path: List[Position] = None
        self.cur_walk_start_time = None

    def start_walking(self, path, start_time):
        self.cur_walk_path = path
        self.cur_walk_start_time = start_time

    def stop_walking(self):
        self.cur_walk_path = None
        self.cur_walk_start_time = None