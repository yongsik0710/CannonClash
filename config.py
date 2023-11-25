import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Levels:
    level_1 = resource_path("Images/Levels/level_1.png")
    level_2 = resource_path("Images/Levels/rainbow.png")


class Texture:
    class Shells:
        basic = resource_path("Images/Shells/ball.png")

    class Cannon:
        basic = resource_path("Images/Cannons/basic.png")
