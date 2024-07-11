from random import randint

class Dish:
    def __init__(self, id, avg_cooking_time):
        self.id = id
        self.avg_cooking_time = avg_cooking_time
    
    def get_new_prob_cooking_time(self):
        return self.avg_cooking_time + randint(-60, 60) # config
    
    def __str__(self):
        return f"Dish {self.id}"
    
    def __repr__(self):
        return f"Dish {self.id}"