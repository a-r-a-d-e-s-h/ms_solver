from board import Board, Tile
from mine_array import MineArray

class Game:
    cascade = True
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = Board(width, height)
        self.mine_array = MineArray(width, height, mines)

    def randomize_mines(self):
        self.mine_array.randomize()

    def start(self):
        self.board.clear()

    def new_game(self):
        self.randomize_mines()
        self.start()

    def neighbour_count(self, row, col):
        neighbours = self.mine_array.neighbours(row, col)
        return sum(self.mine_array.get(*coord) for coord in neighbours)

    def on_board(self, row, col):
        return (0 <= row < self.height) and (0 <= col < self.width)

    def click(self, row, col):
        if not self.on_board(row, col):
            raise RuntimeError("({}, {}) is not within the bounds of the board.".format(row, col))
        if self.mine_array.is_mine(row, col):
            for index, val in enumerate(self.mine_array.array):
                if val:
                    self.board.array[index] = Tile.MINE
            self.board.set(row, col, Tile.BLAST)
        else:
            if self.cascade:
                self.cascade_open(row, col)
            else:
                num = self.neighbour_count(row, col)
                self.board.set(row, col, Tile.num(num))

    def cascade_open(self, row, col):
        to_do = [(row, col)]
        board = self.board
        while to_do:
            row, col = to_do.pop()
            n_count = self.neighbour_count(row, col)
            board.set(row, col, Tile.num(n_count))
            if n_count == 0:
                for (i, j) in self.mine_array.neighbours(row, col):
                    if self.board.get(i, j).is_num():
                        continue
                    if (i, j) in to_do:
                        continue
                    to_do.append((i, j))

    def is_solved(self):
        for row in range(self.height):
            for col in range(self.width):
                mine = self.mine_array.get(row, col)
                if mine == 0:
                    if not self.board.get(row, col).is_num():
                        return False
        return True


    def __str__(self):
        return str(self.board)

