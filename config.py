import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Options:
    class Video:
        display_resolution = [1920, 1080]

    class Audio:
        volume = 1.0


class Resources:
    class Fonts:
        font = resource_path("Fonts/LINESeedKR-Bd.ttf")

    class Effects:
        explosion = resource_path("Images/Effects/explosion.png")
        explosion_2 = resource_path("Images/Effects/explosion_2.png")
        explosion_3 = resource_path("Images/Effects/explosion_3.png")

    class Util:
        current_player = resource_path("Images/Utilities/current_player.png")

    class Sounds:
        class Music:
            lobby = resource_path("Sounds/Background/1.wav")

        class Cannon:
            class Basic:
                shoot = resource_path("Sounds/Cannon/Basic/shoot.wav")
                damage = resource_path("Sounds/Cannon/Basic/damage.wav")

            class Ballista:
                shoot = resource_path("Sounds/Cannon/Ballista/shoot.wav")
                damage = resource_path("Sounds/Cannon/Ballista/damage.wav")

            class FlameCannon:
                shoot = resource_path("Sounds/Cannon/FlameCannon/shoot.wav")
                damage = resource_path("Sounds/Cannon/FlameCannon/damage.wav")

        class Shell:
            class Basic:
                explode = resource_path("Sounds/Shell/Basic/explode.wav")

            class Arrow:
                explode = resource_path("Sounds/Shell/Arrow/explode.wav")

            class Fireball:
                explode = resource_path("Sounds/Shell/Fireball/explode.wav")

        class Util:
            class Button:
                click = resource_path("Sounds/Util/click.wav")

    class Levels:
        class Level1:
            level_image = resource_path("Images/Levels/level_1.png")
            background_image = resource_path("Images/Backgrounds/level_1.png")

        class Level2:
            level_image = resource_path("Images/Levels/level_2.png")
            background_image = resource_path("Images/Backgrounds/level_2.png")

        class Level3:
            level_image = resource_path("Images/Levels/level_3.png")
            background_image = resource_path("Images/Backgrounds/level_3.png")

        class Level4:
            level_image = resource_path("Images/Levels/level_4.png")
            background_image = resource_path("Images/Backgrounds/level_4.png")

    class Cannons:
        class Barrel:
            basic_barrel = resource_path("Images/Cannons/Basic/barrel.png")
            ballista_barrel = resource_path("Images/Cannons/Ballista/barrel.png")
            flame_cannon_barrel = resource_path("Images/Cannons/FlameCannon/barrel.png")

        class Wheel:
            basic_wheel = resource_path("Images/Cannons/Basic/wheel.png")
            ballista_wheel = resource_path("Images/Cannons/Ballista/wheel.png")
            flame_cannon_wheel = resource_path("Images/Cannons/FlameCannon/wheel.png")

    class Shells:
        basic = resource_path("Images/Shells/basic.png")
        arrow = resource_path("Images/Shells/arrow.png")
        fireball = resource_path("Images/Shells/fireball.png")
