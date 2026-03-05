from src.constants import GAME_TITLE, SCREEN_HEIGHT, SCREEN_WIDTH
from src.game import Game


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    game.run()


if __name__ == "__main__":
    main()
