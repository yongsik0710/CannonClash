import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


LEVELS = {
    "test_level": {"level_image": resource_path("Images/Levels/test_level.png"),
                   "background_image": resource_path("Images/Backgrounds/sky.png"),
                   "gravity": 1.0,
                   "air_resistance": 0.0},
    "level_1": {"level_image": resource_path("Images/Levels/level_1.png"),
                "background_image": resource_path("Images/Backgrounds/sky.png"),
                "gravity": 1.0,
                "air_resistance": 0.0},
    "level_2": {"level_image": resource_path("Images/Levels/level_2.png"),
                "background_image": resource_path("Images/Backgrounds/sky.png"),
                "gravity": 1.0,
                "air_resistance": 0.0}
}


class TexturePath:
    class Shells:
        basic = resource_path("Images/Shells/basic_shell.png")

    class Cannon:
        class Barrel:
            barrel_1 = resource_path("Images/Cannons/Cannon_1/barrel.png")
            barrel_2 = resource_path("Images/Cannons/Cannon_2/barrel.png")

        class Wheel:
            wheel_1 = resource_path("Images/Cannons/Cannon_1/wheel.png")
            wheel_2 = resource_path("Images/Cannons/Cannon_2/wheel.png")


CANNONS = {
    1: {"id": 1,
        "name": "Cannon 1",
        "barrel_texture": TexturePath.Cannon.Barrel.barrel_1,
        "wheel_texture": TexturePath.Cannon.Wheel.wheel_1},
    2: {"id": 2,
        "name": "Cannon 2",
        "barrel_texture": TexturePath.Cannon.Barrel.barrel_2,
        "wheel_texture": TexturePath.Cannon.Wheel.wheel_2}
}
