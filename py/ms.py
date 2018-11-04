import ms_game
import simple_solve
from board import Tile

def main():
    game = ms_game.Game(16, 16, 40)
    hit_opening = False
    attempts = 0
    while not hit_opening:
        attempts += 1
        game.new_game()
        game.click(10, 10)
        if game.board.get(10, 10) == Tile.NUM_0:
            hit_opening = True
    print("After {} attempts:".format(attempts))
    print(game)
    result = True
    cycles = 0
    while result:
        cycles += 1
        result = simple_solve.solve(game.board)
    print("After {} naive cycles...".format(cycles))
    print(game)
    

if __name__ == "__main__":
    main()

