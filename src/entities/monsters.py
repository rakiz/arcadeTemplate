# /Users/sebastien.mendez/PycharmProjects/ArcadeTest/src/entities/monsters.py
import arcade # Ajout de l'import arcade
import random # Pour l'exemple de mouvement
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, MONSTER_TEXTURE, MONSTER_MOVEMENT_SPEED, MONSTER_TEXTURES # Importer vitesse
from src.entities.base_entity import BaseEntity # Assure-toi que BaseEntity hérite de arcade.Sprite

class Monster(BaseEntity):
    def __init__(self, center_x=0, center_y=0, texture_file=MONSTER_TEXTURE):
        # Charge une texture spécifique pour chaque monstre
        super().__init__(center_x=center_x, center_y=center_y, texture_file=texture_file)
        self.speed = MONSTER_MOVEMENT_SPEED

        # --- Exemple de mouvement initial aléatoire ---
        self.change_x = random.choice([-self.speed, self.speed])
        self.change_y = random.choice([-self.speed, self.speed])
        # --- Fin de l'exemple de mouvement ---

    def update(self, delta_time: float = 1/60): # delta_time est reçu mais pas forcément utilisé ici
        """ Mise à jour de la position et logique du monstre """

        # --- Logique de mouvement autonome (exemple: rebondir sur les bords) ---
        # (Cette logique est bonne, elle modifie change_x/change_y)
        window = arcade.get_window()
        if window:
            if self.left < 0 and self.change_x < 0:
                self.change_x *= -1
            elif self.right > window.width - 1 and self.change_x > 0:
                self.change_x *= -1
            if self.bottom < 0 and self.change_y < 0:
                self.change_y *= -1
            elif self.top > window.height - 1 and self.change_y > 0:
                self.change_y *= -1
        # --- Fin de l'exemple de mouvement ---

        # Appelle la méthode update du Sprite parent pour appliquer change_x/change_y
        # C'est ici que le mouvement est réellement appliqué à center_x/center_y
        super().update() # Ne pas multiplier par delta_time ici si super().update() le fait déjà ou si la vitesse est en pixels/frame

# --- Classe Monsters utilisant arcade.SpriteList en interne ---
class Monsters:
    def __init__(self):
        # Utiliser une SpriteList au lieu d'une liste Python standard
        self.sprite_list: arcade.SpriteList = arcade.SpriteList()
        # Pas besoin de référence directe si on n'interagit pas individuellement avec les monstres depuis Game

    def setup(self):
        """ Initialise plusieurs monstres """
        for i in range(4):  # Crée 4 monstres
            monster_start_x = random.randint(50, SCREEN_WIDTH - 50)
            monster_start_y = random.randint(50, SCREEN_HEIGHT - 50)
            texture_file = random.choice(MONSTER_TEXTURES)  # Choisit une texture aléatoire
            monster = Monster(center_x=monster_start_x, center_y=monster_start_y, texture_file=texture_file)
            self.sprite_list.append(monster)

    def update(self, delta_time):
        """ Met à jour tous les monstres via la SpriteList """
        # La SpriteList appelle .update(delta_time) sur chaque sprite contenu
        self.sprite_list.update(delta_time) # Assure-toi que Monster.update est bien défini

    def draw(self):
        """ Dessine tous les monstres via la SpriteList """
        # La SpriteList appelle .draw() sur chaque sprite contenu (optimisé)
        self.sprite_list.draw()

