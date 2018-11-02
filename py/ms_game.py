from enum import Enum
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
    def __str__(self):
        return '.'

class Mine(Tile):
    def __str__(self):
        return 'm'

class BlastedMine(Tile):
    def __str__(self):
        return 'M'

class Board:
    display_borders = True
    unicode_chars = True
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.init_array()

    def init_array(self):
        self.array = [[Unopened() for col in range(self.width)] for row in range(self.height)]

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
                    if i != row or j != col:
                        yield (i, j)
        return neighbour_iter()

    def __iter__(self):
        for row in range(self.height):
            for col in range(self.width):
                yield (row, col)

    def get_tile(self, row, col):
        return self.array[row][col]

class GameState(Enum):
    INACTIVE = 1
    ACTIVE = 2
    BLASTED = 3
    SOLVED = 4
    

class Game:
    cascade = True
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.mine_array = MineArray(width, height, mines)
        self.board = Board(width, height)

        self.in_play = False
        self.status = GameState.INACTIVE

    def randomize_mines(self):
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

    def new_game(self):
        self.randomize_mines()
        self.start()

    def start(self):
        self.status = GameState.ACTIVE
        self.board = Board(self.width, self.height)

    def click(self, row, col):
        if not self.status == GameState.ACTIVE:
            raise RuntimeError("Cannot click square, game inactive")
        board = self.board

        tile = board.get_tile(row, col)
        if self.is_mine(row, col):
            self.status = GameState.BLASTED
            for (i, j) in board:
                if self.is_mine(i, j):
                    board.array[i][j] = Mine()
            board.array[row][col] = BlastedMine()
        else:
            if self.cascade:
                self.cascade_open(row, col)
            else:
                n_count = self.neighbour_count(row, col)
                board.array[row][col] = Number(n_count)

    def cascade_open(self, row, col):
        to_do = [(row, col)]
        board = self.board
        while to_do:
            row, col = to_do.pop()
            n_count = self.neighbour_count(row, col)
            board.array[row][col] = Number(n_count)
            if n_count == 0:
                for (i, j) in self.board.neighbours(row, col):
                    if type(self.board.get_tile(i, j) ) is Number:
                        continue
                    if (i, j) in to_do:
                        continue
                    to_do.append((i, j))
                    
    def is_mine(self, row, col):
        return bool(self.mine_array.array[row][col])

    def neighbour_count(self, row, col):
        count = 0
        for (i, j) in self.board.neighbours(row, col):
            if self.is_mine(i, j):
                count += 1
        return count

