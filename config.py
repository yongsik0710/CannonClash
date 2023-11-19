import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Texture:
    class Blocks:
        none = resource_path("Images/Blocks/none.png")
        air_transparent = resource_path("Images/Blocks/air_transparent.png")
        air = resource_path("Images/Blocks/air.png")
        grass = resource_path("Images/Blocks/grass.png")
        dirt = resource_path("Images/Blocks/dirt.png")
        stone = resource_path("Images/Blocks/stone.png")
        iron = resource_path("Images/Blocks/iron.png")

    class Shells:
        basic = resource_path("Images/Shells/ball.png")

    class Buttons:
        button = resource_path("Images/Buttons/button.png")
