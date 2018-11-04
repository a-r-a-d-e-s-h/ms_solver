from enum import Enum
from board import Tile

def solve(board):
    width = board.width
    height = board.height
    safes = []
    mines = []
    for row in range(height):
        for col in range(width):
            tile = board.get(row, col)
            if tile.is_num() and tile != Tile.NUM_0:
                res = simple_assess(board, row, col)
                if res == Decision.SAFE:
                    safes.append((row, col))
                elif res == Decision.MINE:
                    mines.append((row, col))
    for (row, col) in safes:
        for (i, j) in board.neighbours(row, col):
            if board.get(i, j) == Tile.UNOPENED:
                board.set(i, j, Tile.SAFE)
    for (row, col) in mines:
        for (i, j) in board.neighbours(row, col):
            if board.get(i, j) == Tile.UNOPENED:
                board.set(i, j, Tile.FLAG)
    return (safes or mines)
        

class Decision(Enum):
    SAFE = 1
    MINE = 2
    UNKNOWN = 3
    SOLVED = 4

def simple_assess(board, row, col):
    tile = board.get(row, col)
    value = tile.value
    mines = 0
    safes = 0
    for count, (i, j) in enumerate(board.neighbours(row, col)):
        next_tile = board.get(i, j)
        if next_tile == Tile.FLAG:
            mines += 1
        if next_tile.is_safe():
            safes += 1
    tot_neighbours = count + 1
    unopened = tot_neighbours - mines - safes
    if unopened == 0:
        return Decision.SOLVED
    if mines == value:
        return Decision.SAFE
    if unopened + mines == value:
        return Decision.MINE
    return Decision.UNKNOWN

