import ms_game

def main():
    game = ms_game.Game(16, 16, 40)
    game.new_game()
    game.click(20, 20)
    print(game)

if __name__ == "__main__":
    main()

