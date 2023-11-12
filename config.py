import pygame
import os


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("images", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()


class Texture:
    air = load_png("Air.png")
    grass = load_png("grass.png")
    dirt = load_png("dirt.png")
    stone = load_png("stone.png")
    iron = load_png("iron.png")
