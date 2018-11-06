from board import Tile

class Solver:
    def __init__(self, game):
        self.game = game
        self.width = game.width
        self.height = game.height
        self.mines = game.mines

    def do_solve(self):
        board = self.game.board
        for row in range(self.height):
            for col in range(self.width):
                if self.examine(row, col):
                    return True
        return False # Could make no progress

    def examine(self, row, col):
        board = self.game.board
        tile = board.get(row, col)
        if tile.is_num():
            unopened = []
            flags = []
            safes = []
            neighbours = board.neighbours(row, col)
            for nbour in neighbours:
                ntile = board.get(*nbour)
                if ntile == Tile.UNOPENED:
                    unopened.append(nbour)
                elif ntile.is_safe():
                    safes.append(nbour)
                elif ntile == Tile.FLAG:
                    flags.append(nbour)
            if not unopened: # Square is solved. Don't continue.
                return False
            if len(unopened) + len(flags) == tile.value:
                for i, j in unopened:
                    board.set(i, j, Tile.FLAG)
                    return True
            if len(flags) == tile.value:
                i, j = unopened[0]
                self.game.click(i, j)
                return True
        return False # We took no action

def simple_solve_test():
    import ms_game
    test_run = 1000
    game = ms_game.Game(8, 8, 10)
    first_click = (0,0)
    solved = 0
    failed = 0
    for count in range(test_run):
        hit_opening = False
        attempts = 0
        while not hit_opening:
            attempts += 1
            game.new_game()
            game.click(*first_click)
            if game.board.get(*first_click) == Tile.NUM_0:
                hit_opening = True
        solver = Solver(game)   
        result = True
        while result:
            result = solver.do_solve()
        if game.is_solved():
            solved += 1
            print(game)
        else:
            failed += 1
        print("{}/{}".format(solved, count + 1))


