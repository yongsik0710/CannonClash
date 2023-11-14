import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Texture:
    none = resource_path("images/none.png")
    air = resource_path("images/air.png")
    grass = resource_path("images/grass.png")
    dirt = resource_path("images/dirt.png")
    stone = resource_path("images/stone.png")
    iron = resource_path("images/iron.png")
