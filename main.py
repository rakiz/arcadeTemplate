import arcade
from src.game import Game

def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
