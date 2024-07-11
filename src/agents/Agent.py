from src.utils.utils import Position
from typing import List

class Agent():
    def __init__(self, id, position: Position = None, type = "Agent"):
        self.id = id
        self.position: Position = position
        self.cur_walk_path: List[Position] = None
        self.cur_walk_start_time = None
        self.type = type

    def start_walking(self, path, start_time, verbose):
        self.cur_walk_path = path
        self.cur_walk_start_time = start_time
        if verbose:
            print(f'\t{self.type} {self.id} started walking {path} at time {start_time}.')

    def stop_walking(self, time, verbose):
        if self.cur_walk_start_time is not None: # si está caminando
            self.position = self.get_position_at(time)
            self.cur_walk_path = None
            self.cur_walk_start_time = None
            if verbose:
                print(f'\t{self.type} {self.id} stoped walking at time {time}, position {self.position}.')
    
    def get_position_at(self, time): # retorna la posición del agente en el tiempo `time`
        if self.cur_walk_start_time is None: 
            # si no está caminando
            return self.position # posición actual
        if time - self.cur_walk_start_time >= len(self.cur_walk_path): 
            # si se pregunta por un tiempo posterior a que termine su camino actual (no debería pasar)
            print("\tWARNING: Unexpected behaviour")
            return self.cur_walk_path[-1] # posición final del camino actual
        return self.cur_walk_path[time - self.cur_walk_start_time] # posición del camino en la que estaría
    
    def __str__(self):
        return f"{self.type} {self.id}"
    
    def __repr__(self):
        return f"{self.type} {self.id}"