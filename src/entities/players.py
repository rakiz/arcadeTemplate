# /Users/sebastien.mendez/PycharmProjects/ArcadeTest/src/entities/players.py
from __future__ import annotations

import arcade
from src.constants import SCREEN_WIDTH, PLAYER_TEXTURE, PLAYER_MOVEMENT_SPEED
from src.entities.base_entity import BaseEntity

class Player(BaseEntity):
    def __init__(self, center_x=0, center_y=0, key_mapping=None):
        super().__init__(center_x=center_x, center_y=center_y, texture_file=PLAYER_TEXTURE)
        self.change_x = 0
        self.change_y = 0
        self.speed = PLAYER_MOVEMENT_SPEED
        # Définir le mapping des touches, avec des valeurs par défaut si non fourni
        self.key_mapping = key_mapping or {
            "left": arcade.key.LEFT,
            "right": arcade.key.RIGHT,
            "up": arcade.key.UP,
            "down": arcade.key.DOWN
        }

    def update(self, delta_time: float = 1/60):
        """ Met à jour la position du joueur """
        # La méthode update de arcade.Sprite applique change_x et change_y
        super().update()

        # --- Optionnel : Garder le joueur dans l'écran ---
        window = arcade.get_window()
        if window:
            if self.left < 0:
                self.left = 0
            elif self.right > window.width - 1:
                self.right = window.width - 1
            if self.bottom < 0:
                self.bottom = 0
            elif self.top > window.height - 1:
                self.top = window.height - 1

    def on_key_press(self, key, modifiers):
        if key == self.key_mapping["left"]:
            self.change_x -= self.speed
        elif key == self.key_mapping["right"]:
            self.change_x += self.speed
        elif key == self.key_mapping["up"]:
            self.change_y += self.speed
        elif key == self.key_mapping["down"]:
            self.change_y -= self.speed

    def on_key_release(self, key, modifiers):
        if key == self.key_mapping["left"]:
            self.change_x += self.speed
        elif key == self.key_mapping["right"]:
            self.change_x -= self.speed
        elif key == self.key_mapping["up"]:
            self.change_y -= self.speed
        elif key == self.key_mapping["down"]:
            self.change_y += self.speed

# --- Classe Players utilisant arcade.SpriteList en interne ---
class Players:
    def __init__(self):
        # Utiliser une SpriteList au lieu d'une liste Python standard
        self.sprite_list: arcade.SpriteList = arcade.SpriteList()

    def setup(self):
        """ Initialise les joueurs """
        player_start_x = SCREEN_WIDTH / 2
        player_start_y = 50
        # Créer l'instance du joueur principal avec un jeu de touches personnalisé
        player = Player(
            center_x=player_start_x, 
            center_y=player_start_y, 
            key_mapping={
                "left": arcade.key.LEFT,
                "right": arcade.key.RIGHT,
                "up": arcade.key.UP,
                "down": arcade.key.DOWN
            }
        )
        # Ajouter l'instance à la SpriteList interne
        self.sprite_list.append(player)

        # Exemple : Ajouter un deuxième joueur avec un autre jeu de touches
        player = Player(
            center_x=player_start_x + 100, 
            center_y=player_start_y, 
            key_mapping={
                "left": arcade.key.A,
                "right": arcade.key.D,
                "up": arcade.key.W,
                "down": arcade.key.S
            }
        )
        self.sprite_list.append(player)

    def on_key_press(self, key, modifiers):
        """ Délègue les entrées clavier à tous les joueurs """
        for player in self.sprite_list:
            player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """ Délègue les relâchements de touches à tous les joueurs """
        for player in self.sprite_list:
            player.on_key_release(key, modifiers)

    def update(self, delta_time):
        """ Met à jour tous les joueurs via la SpriteList """
        # La SpriteList appelle .update(delta_time) sur chaque sprite contenu
        self.sprite_list.update(delta_time)

    def draw(self):
        """ Dessine tous les joueurs via la SpriteList """
        # La SpriteList appelle .draw() sur chaque sprite contenu (optimisé)
        self.sprite_list.draw()

