from enum import Enum
from grid import Grid

class Tile(Enum):
    NUM_0 = 0
    NUM_1 = 1
    NUM_2 = 2
    NUM_3 = 3
    NUM_4 = 4
    NUM_5 = 5
    NUM_6 = 6
    NUM_7 = 7
    NUM_8 = 8
    UNOPENED = '.'
    MINE = 'm'
    BLAST = 'M'
    FLAG = '^'
    SAFE = '_'

    @classmethod
    def num(cls, n):
        return cls(n)

    def is_num(self):
        return (type(self.value) is int) and (0 <= self.value <= 8)

    def is_safe(self):
        return self.is_num() or (self == Tile.SAFE)

    def __str__(self):
        if self.value == 0:
            return ' '
        else:
            return str(self.value)


class Board(Grid):
    def __init__(self, width, height):
        super().__init__(width, height, Tile.UNOPENED)

    def clear(self):
        self.init_array()
