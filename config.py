import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Levels:
    test_level = {"level_image": resource_path("Images/Levels/test_level.png"),
                  "background_image": resource_path("Images/Backgrounds/sky.png"),
                  "gravity": 1.0,
                  "air_resistance": 0.0}
    level_1 = {"level_image": resource_path("Images/Levels/level_1.png"),
               "background_image": resource_path("Images/Backgrounds/sky.png"),
               "gravity": 1.0,
               "air_resistance": 0.0}
    level_2 = {"level_image": resource_path("Images/Levels/level_2.png"),
               "background_image": resource_path("Images/Backgrounds/sky.png"),
               "gravity": 1.0,
               "air_resistance": 0.0}


class Texture:
    class Shells:
        basic = resource_path("Images/Shells/ball.png")

    class Cannon:
        class Barrel:
            cannon_1 = resource_path("Images/Cannons/cannon_1.png")

        class Wheel:
            wheel_1 = resource_path("Images/Cannons/wheel_1.png")
