import ms_game

def main():
    game = ms_game.Game(16, 16, 40)
    game.new_random()
    print(game.solved_board())

if __name__ == "__main__":
    main()

