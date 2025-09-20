import arcade
import os
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Space Invaders"

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_INVADER = 0.4
SPRITE_SCALING_LASER = 0.8
SPRITE_SCALING_BARRIER = 0.15

PLAYER_START_Y = 50
PLAYER_MOVEMENT_SPEED = 7
LASER_SPEED = 6

INVADER_ROWS = 5
INVADER_COLUMNS = 11
INVADER_X_SPACING = 50
INVADER_Y_SPACING = 40
INVADER_START_X = (SCREEN_WIDTH - (INVADER_COLUMNS - 1) * INVADER_X_SPACING) / 2
INVADER_START_Y = SCREEN_HEIGHT - 100
INVADER_MOVEMENT_SPEED = 2
INVADER_DROP_DISTANCE = 15
INVADER_SPEED_INCREASE = 0.1

BARRIER_COUNT = 4
BARRIER_START_Y = 150
BARRIER_X_START = SCREEN_WIDTH * 0.15
BARRIER_X_END = SCREEN_WIDTH * 0.85
BARRIER_STRUCTURE = [
    "  XXXX  ",
    " XXXXXX ",
    "XXXXXXXX",
    "XXX  XXX",
    "XX    XX"
]


class Player(arcade.Sprite):
    """Player Sprite (Tank)"""
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        if self.left < 10:
            self.left = 10
        elif self.right > SCREEN_WIDTH - 10:
            self.right = SCREEN_WIDTH - 10


class Invader(arcade.Sprite):
    """Invader Sprite (Alien)"""
    pass


class BarrierBlock(arcade.Sprite):
    """Barrier Block Sprite"""
    pass


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_result = None  # Résultat de la partie (win ou lose)
        self.keys_pressed = set()  # Suivi des touches enfoncées
        self.current_direction = None  # Direction actuelle
        self.player_list = None
        self.invader_list = None
        self.barrier_list = None
        self.player_laser_list = None
        self.particle_list = None

        self.player_sprite = None
        self.invader_direction = INVADER_MOVEMENT_SPEED
        self.invader_current_speed = INVADER_MOVEMENT_SPEED

        self.game_state = "playing"  # Nouvel état de jeu
        arcade.set_background_color(arcade.color.BLACK)

        # Préparer les textes pour éviter les appels fréquents à draw_text
        self.victory_text = arcade.Text(
            "VICTOIRE !", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
            arcade.color.WHITE, font_size=30, anchor_x="center"
        )
        self.defeat_text = arcade.Text(
            "DÉFAITE !", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
            arcade.color.RED, font_size=30, anchor_x="center"
        )
        self.restart_text = arcade.Text(
            "Appuyez sur une touche pour recommencer", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
            arcade.color.WHITE, font_size=20, anchor_x="center"
        )

    def setup(self):
        """Set up the game"""
        self.game_state = "playing"  # Réinitialise l'état de jeu
        self.player_list = arcade.SpriteList()
        self.invader_list = arcade.SpriteList()
        self.barrier_list = arcade.SpriteList()
        self.player_laser_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()

        # Player
        self.player_sprite = Player(":resources:images/topdown_tanks/tank_blue.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # Invaders
        invader_images = [
            ":resources:images/space_shooter/meteorGrey_big1.png",
            ":resources:images/space_shooter/meteorGrey_big2.png",
            ":resources:images/space_shooter/meteorGrey_big3.png"
        ]
        for row in range(INVADER_ROWS):
            for col in range(INVADER_COLUMNS):
                x = INVADER_START_X + col * INVADER_X_SPACING
                y = INVADER_START_Y - row * INVADER_Y_SPACING
                img = invader_images[row % len(invader_images)]
                invader = Invader(img, SPRITE_SCALING_INVADER)
                invader.center_x = x
                invader.center_y = y
                self.invader_list.append(invader)

        # Barriers
        barrier_spacing = (BARRIER_X_END - BARRIER_X_START) / (BARRIER_COUNT - 1)
        for i in range(BARRIER_COUNT):
            barrier_center_x = BARRIER_X_START + i * barrier_spacing
            for row_index, row_str in enumerate(BARRIER_STRUCTURE):
                for col_index, char in enumerate(row_str):
                    if char == 'X':
                        block_x = barrier_center_x - (len(row_str) / 2 - col_index) * 10 * SPRITE_SCALING_BARRIER
                        block_y = BARRIER_START_Y - row_index * 10 * SPRITE_SCALING_BARRIER
                        barrier_block = BarrierBlock(":resources:images/tiles/boxCrate_double.png",
                                                     SPRITE_SCALING_BARRIER)
                        barrier_block.center_x = block_x
                        barrier_block.center_y = block_y
                        self.barrier_list.append(barrier_block)

    def fire_player_laser(self):
        """Créer et tirer un laser depuis le joueur avec des particules"""
        # Créer le laser
        laser = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)
        laser.center_x = self.player_sprite.center_x
        laser.bottom = self.player_sprite.top
        laser.change_y = LASER_SPEED
        laser.angle = 270  # Oriente le laser verticalement
        self.player_laser_list.append(laser)

        # Générer des particules
        for _ in range(10):  # Nombre de particules
            particle = arcade.SpriteCircle(3, arcade.color.BLUE)
            particle.center_x = self.player_sprite.center_x + random.uniform(-5, 5)
            particle.center_y = self.player_sprite.top
            particle.change_x = random.uniform(-1, 1)
            particle.change_y = random.uniform(1, 3)
            particle.alpha = 255  # Opacité initiale
            self.particle_list.append(particle)

    def on_update(self, delta_time):
        """Game logic"""
        if self.game_state != "playing":
            return

        self.player_list.update()
        self.player_laser_list.update()
        self.particle_list.update()

        # Mise à jour des particules
        for particle in self.particle_list:
            particle.alpha -= 5
            if particle.alpha <= 0:
                particle.remove_from_sprite_lists()

        # Déplacement des envahisseurs
        for invader in self.invader_list:
            invader.center_x += self.invader_direction

        # Vérification des rebonds sur les murs
        if self.invader_list:
            left_most = min(invader.left for invader in self.invader_list)
            right_most = max(invader.right for invader in self.invader_list)

            if left_most <= 0 or right_most >= SCREEN_WIDTH:
                self.invader_direction *= -1
                for invader in self.invader_list:
                    invader.center_y -= INVADER_DROP_DISTANCE

        # Vérification des collisions entre lasers et envahisseurs
        for laser in self.player_laser_list:
            hit_list = arcade.check_for_collision_with_list(laser, self.invader_list)
            if hit_list:
                laser.remove_from_sprite_lists()
                for invader in hit_list:
                    invader.remove_from_sprite_lists()

        # Vérifiez si tous les aliens sont détruits
        if not self.invader_list:
            self.game_state = "game_over"
            self.game_result = "win"

        # Vérification des collisions entre les envahisseurs et le joueur
        if arcade.check_for_collision_with_list(self.player_sprite, self.invader_list):
            self.game_state = "game_over"
            self.game_result = "lose"

    def on_draw(self):
        """Render the screen"""
        self.clear()
        self.player_list.draw()
        self.invader_list.draw()
        self.barrier_list.draw()
        self.player_laser_list.draw()
        self.particle_list.draw()

        if self.game_state == "game_over":
            if self.game_result == "win":
                self.victory_text.draw()
            elif self.game_result == "lose":
                self.defeat_text.draw()
            self.restart_text.draw()

    def on_key_press(self, key, modifiers):
        """Gérer les touches pressées"""
        if self.game_state == "game_over":
            self.setup()  # Redémarre le jeu
            return

        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.current_direction = key  # Met à jour la direction actuelle
            if key == arcade.key.LEFT:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            self.fire_player_laser()

    def on_key_release(self, key, modifiers):
        """Arrêter le mouvement du joueur lorsque les touches sont relâchées"""
        if key == self.current_direction:  # Arrête uniquement si la direction actuelle est relâchée
            self.current_direction = None
            self.player_sprite.change_x = 0

def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()