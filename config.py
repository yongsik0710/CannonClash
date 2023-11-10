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
    air = pygame.image.load("images/air.png")
    grass = pygame.image.load("images/grass.png")
    dirt = pygame.image.load("images/dirt.png")
    stone = pygame.image.load("images/stone.png")
    iron = pygame.image.load("images/iron.png")
