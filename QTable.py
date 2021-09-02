import numpy as np

class qtable:
    def __init__(self, game_size):
        # Size is game size * game size * 1 * 1
        # game size * game size - snake head location
        # 1 * 1 - apple location
        self.Q = np.zeros((
            game_size, 
            game_size, 
            1, 
            1
        ))