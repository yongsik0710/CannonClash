import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Levels:
    class TestLevel:
        level_image = resource_path("Images/Levels/test_level.png")
        background_image = resource_path("Images/Backgrounds/sky.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(100, 100), (250, 200), (1800, 100), (2200, 300), (400, 100), (800, 100)]

    class Level1:
        level_image = resource_path("Images/Levels/level_1.png")
        background_image = resource_path("Images/Backgrounds/sky.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(100, 100), (250, 200), (1800, 100), (2200, 300), (400, 100), (800, 100)]

    class Level2:
        level_image = resource_path("Images/Levels/level_2.png")
        background_image = resource_path("Images/Backgrounds/sky.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(100, 100), (250, 200), (1800, 100), (2200, 300), (400, 100), (800, 100)]


class TexturePath:
    class Shells:
        basic = resource_path("Images/Shells/basic_shell.png")

    class Cannon:
        class Barrel:
            barrel_1 = resource_path("Images/Cannons/Basic/barrel_1.png")
            barrel_2 = resource_path("Images/Cannons/Test/barrel.png")

        class Wheel:
            wheel_1 = resource_path("Images/Cannons/Basic/wheel_1.png")
            wheel_2 = resource_path("Images/Cannons/Test/wheel.png")

    class Util:
        current_player = resource_path("Images/Utilities/current_player.png")
