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
        spawn_points = [(100, 100), (100, 200), (2000, 100), (2000, 300), (300, 100), (700, 100)]

    class Level1:
        level_image = resource_path("Images/Levels/level_1.png")
        background_image = resource_path("Images/Backgrounds/sky.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(100, 100), (100, 200), (200, 100), (500, 300), (300, 100), (700, 100)]

    class Level2:
        level_image = resource_path("Images/Levels/rainbow.png")
        background_image = resource_path("Images/Backgrounds/sky.png")
        gravity = 1.0
        air_resistance = 0.0
        spawn_points = [(100, 100), (100, 200), (200, 100), (500, 300), (300, 100), (700, 100)]


class TexturePath:
    class Shells:
        basic = resource_path("Images/Shells/basic_shell.png")

    class Cannon:
        class Barrel:
            barrel_1 = resource_path("Images/Cannons/Basic/barrel.png")
            barrel_2 = resource_path("Images/Cannons/Cannon_2/barrel.png")

        class Wheel:
            wheel_1 = resource_path("Images/Cannons/Basic/wheel.png")
            wheel_2 = resource_path("Images/Cannons/Cannon_2/wheel.png")
