from config import *
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


class Block(pygame.sprite.Sprite):
    texture = ""
    blastResistance = 0
    passable = False

    def __init__(self):
        self.health = 100
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = self.texture
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def update(self, x, y):
        self.rect = (x, y)


class Air(Block):
    texture = Texture.air
    blastResistance = 0
    passable = True


class Grass(Block):
    texture = Texture.grass
    blastResistance = 10


class Dirt(Block):
    texture = Texture.dirt
    blastResistance = 0


class Stone(Block):
    texture = Texture.stone
    blastResistance = 30


class Iron(Block):
    texture = Texture.iron
    blastResistance = 70
