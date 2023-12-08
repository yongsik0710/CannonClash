import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class FontPath:
    font = resource_path("Fonts/LINESeedKR-Bd.ttf")


class Levels:
    class Level1:
        level_image = resource_path("Images/Levels/level_1.png")
        background_image = resource_path("Images/Backgrounds/snowman.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(350, 925), (900, 930), (1700, 925), (2300, 845), (3000, 890), (4000, 910)]

    class Level2:
        level_image = resource_path("Images/Levels/level_2.png")
        background_image = resource_path("Images/Backgrounds/christmas_ornament.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(270, 540), (1150, 665), (1900, 1010), (2700, 1140), (3000, 360), (3800, 710)]

    class Level3:
        level_image = resource_path("Images/Levels/level_3.png")
        background_image = resource_path("Images/Backgrounds/snow.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(100, 100), (250, 200), (1800, 100), (2200, 300), (400, 100), (800, 100)]

    class Level4:
        level_image = resource_path("Images/Levels/level_4.png")
        background_image = resource_path("Images/Backgrounds/night.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(350, 440), (895, 600), (1800, 805), (2600, 790), (3150, 750), (3950, 585)]


class TexturePath:
    class Shells:
        basic = resource_path("Images/Shells/basic.png")
        arrow = resource_path("Images/Shells/arrow.png")
        fireball = resource_path("Images/Shells/fireball.png")

    class Cannons:
        class Barrel:
            basic_barrel = resource_path("Images/Cannons/Basic/barrel.png")
            ballista_barrel = resource_path("Images/Cannons/Ballista/barrel.png")
            flame_cannon_barrel = resource_path("Images/Cannons/FlameCannon/barrel.png")

        class Wheel:
            basic_wheel = resource_path("Images/Cannons/Basic/wheel.png")
            ballista_wheel = resource_path("Images/Cannons/Ballista/wheel.png")
            flame_cannon_wheel = resource_path("Images/Cannons/FlameCannon/wheel.png")

    class Util:
        current_player = resource_path("Images/Utilities/current_player.png")
