import arcade
import os

class BaseEntity(arcade.Sprite):
    def __init__(self, center_x=0, center_y=0, texture_file=None):
        super().__init__(center_x=center_x, center_y=center_y)
        if texture_file:
            if not os.path.isfile(texture_file):
                raise FileNotFoundError(f"Texture file not found: {texture_file}")
            self.texture = arcade.load_texture(texture_file)
        else:
            raise ValueError("A valid texture file must be provided.")  # Ajout d'une vérification
        # La méthode draw est déjà fournie par arcade.Sprite

    def update(self, delta_time: float = 1/60):
        """ Méthode update commune à toutes les entités. """
        super().update()  # Appeler la méthode parent avec delta_time

    def on_key_press(self, key, modifiers):
        """ Gère les entrées clavier (à surcharger si nécessaire) """
        pass

    def on_key_release(self, key, modifiers):
        """ Gère les relâchements de touches (à surcharger si nécessaire) """
        pass

