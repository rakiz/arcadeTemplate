# /Users/sebastien.mendez/PycharmProjects/ArcadeTest/src/game.py
import arcade
import sys
import os

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if (src_path not in sys.path):
    sys.path.append(src_path)

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from src.entities.players import Players
from src.entities.monsters import Monsters

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)

        # --- Gestionnaires pour les entités ---
        self.players = Players()
        self.monsters = Monsters()

    def setup(self):
        """ Initialisation du jeu """
        self.players.setup()
        self.monsters.setup()

    def on_draw(self):
        """ Dessiner les éléments du jeu """
        self.clear()
        self.players.draw()
        self.monsters.draw()

    def on_key_press(self, key, modifiers):
        """ Appelé quand une touche est pressée """
        self.players.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """ Appelé quand une touche est relâchée """
        self.players.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        """ Logique de jeu appelée à chaque frame """
        self.players.update(delta_time)
        self.monsters.update(delta_time)
