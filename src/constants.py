from arcade.resources import resolve  # Remplacement de resolve_resource_path

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ArcadeTest"

PLAYER_MOVEMENT_SPEED = 5
MONSTER_MOVEMENT_SPEED = 2

# Chemins des textures
PLAYER_TEXTURE = resolve(":resources:images/animated_characters/female_person/femalePerson_idle.png")
MONSTER_TEXTURE = resolve(":resources:images/enemies/slimePurple.png")

MONSTER_TEXTURES = [
    resolve(":resources:images/enemies/wormGreen.png"),
    resolve(":resources:images/enemies/wormPink.png"),
    resolve(":resources:images/enemies/slimeBlock.png"),
    resolve(":resources:images/enemies/slimePurple.png"),
    resolve(":resources:images/enemies/slimeBlue.png"),
    resolve(":resources:images/enemies/slimeGreen.png")
    # Supprimé slimeRed.png car il n'existe pas dans les ressources Arcade
]



