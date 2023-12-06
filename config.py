import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class FontPath:
    font = resource_path("Fonts/EliceDXNeolli-Medium.ttf")
    font_2 = resource_path("Fonts/LINESeedKR-Bd.ttf")


class Levels:
    class Level1:
        level_image = resource_path("Images/Levels/level_1.png")
        background_image = resource_path("Images/Backgrounds/sky.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(100, 100), (250, 200), (1800, 100), (2200, 300), (400, 100), (800, 100)]

    class Level2:
        level_image = resource_path("Images/Levels/level_2.png")
        background_image = resource_path("Images/Backgrounds/christmas_ornament.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(100, 100), (250, 200), (1800, 100), (2200, 300), (400, 100), (800, 100)]

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
        spawn_points = [(100, 100), (250, 200), (1800, 100), (2200, 300), (400, 100), (800, 100)]


class TexturePath:
    class Shells:
        basic = resource_path("Images/Shells/basic.png")

    class Cannon:
        class Barrel:
            basic_barrel = resource_path("Images/Cannons/Basic/barrel.png")
            ballista_barrel = resource_path("Images/Cannons/Ballista/barrel.png")

        class Wheel:
            basic_wheel = resource_path("Images/Cannons/Basic/wheel.png")
            ballista_wheel = resource_path("Images/Cannons/Ballista/wheel.png")

    class Util:
        current_player = resource_path("Images/Utilities/current_player.png")
