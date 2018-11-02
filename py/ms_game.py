import random

class MineArray:
    display_borders = True
    unicode_chars = True
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        if (self.mines < 0) or (self.mines > width * height):
            raise RuntimeError("Number of mines must be non-negative and non exceed the number of squares on the board.")
        self.array = [[0]*width for __ in range(height)]

    def clear(self):
        array = self.array
        for row in range(self.height):
            for col in range(self.width):
                self.array[row][col] = 0

    def randomize(self):
        squares = self.width * self.height
        placed = 0
        self.clear()
        while placed < self.mines:
            new_square = random.randint(0, squares - 1)
            col = new_square % self.width
            row = new_square // self.width
            if self.array[row][col] == 0:
                self.array[row][col] = 1
                placed += 1

    def __str__(self):
        rows = []
        for row in self.array:
            rows.append(' '.join('m' if elem else '.' for elem in row))
        if self.display_borders:
            lines = []
            if self.unicode_chars:
                top_line = '╔' + (2*self.width+1)*'═' + '╗'
                bot_line = '╚' + (2*self.width+1)*'═' + '╝'
                rows = ['║ ' + row + ' ║' for row in rows]
                lines = [top_line] + rows + [bot_line]
                return '\n'.join(lines)
            else:
                top_line = '+' + (2*self.width+1)*'-' + '+'
                rows = ['| ' + row + ' |' for row in rows]
                lines = [top_line] + rows + [top_line]
                return '\n'.join(lines)
        else:
            return '\n'.join(rows)

class Tile:
    pass

class Number(Tile):
    def __init__(self, n=0):
        self.n = n

    def __add__(self, val):
        self.n += val
        return self

    def __sub__(self, val):
        self.n -= val
        return self

    def __str__(self):
        return str(self.n) if self.n else ' '

class Unopened(Tile):
    pass

class Mine(Tile):
    def __str__(self):
        return 'm'

class Board:
    display_borders = True
    unicode_chars = True
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.init_array()

    def init_array(self):
        self.array = [[Number() for col in range(self.width)] for row in range(self.height)]

    def __str__(self):
        array = self.array
        rows = [' '.join(str(item) for item in row) for row in array]
        if self.display_borders:
            if self.unicode_chars:
                top_line = '╔' + (2*self.width-1)*'═' + '╗'
                bot_line = '╚' + (2*self.width-1)*'═' + '╝'
                rows = ['║' + row + '║' for row in rows]
                lines = [top_line] + rows + [bot_line]
            else:
                top_bot = '+' + (2*self.width-1)*'-' + '+'
                rows = ['|' + row + '|' for row in rows]
                lines = [top_bot] + rows + [top_bot]
            return '\n'.join(lines)
        else:
            return '\n'.join(rows)

    def neighbours(self, row, col):
        def neighbour_iter():
            top = max(row-1, 0)
            bot = min(row+1, self.height - 1)
            left = max(col-1, 0)
            right = min(col+1, self.width - 1)
            for i in range(top, bot + 1):
                for j in range(left, right + 1):
                    yield (i, j)
        return neighbour_iter()

class Game:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.mine_array = MineArray(width, height, mines)

    def new_random(self):
        self.mine_array.randomize()

    def solved_board(self):
        board = Board(self.width, self.height)
        mine_array = self.mine_array
        for row in range(mine_array.height):
            for col in range(mine_array.width):
                value = mine_array.array[row][col]
                if value == 0:
                    continue
                board.array[row][col] = Mine()
                for (i, j) in board.neighbours(row, col):
                    if mine_array.array[i][j] == 0:
                        board.array[i][j] += 1
        return board

