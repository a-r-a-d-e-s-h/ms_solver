import random

from grid import Grid

class MineArray(Grid):
    def __init__(self, width, height, mines):
        if (mines < 0) or (mines > width*height):
            raise RuntimeError("Error. Number of mines must be non-negative and not exceed the board area.")
        super().__init__(width, height, default=0)
        self.mines = mines

    def is_mine(self, row, col):
        return bool(self.get(row, col))

    def randomize(self):
        self.clear()
        squares = self.width * self.height
        total_placed = 0
        while total_placed < self.mines:
            rand_index = random.randint(0, squares - 1)
            if self.array[rand_index] == 0:
                total_placed += 1
                self.array[rand_index] = 1

    def clear(self):
        self.init_array()

    def val_to_string(self, val):
        return 'm' if val else '.'
