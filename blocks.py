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
    id = 0
    texture = Texture.none
    blastResistance = 0
    passable = False

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.x = x
        self.y = y
        self.texture = load_png(self.texture)
        self.image, self.rect = self.texture
        self.rect = self.rect.move((120 * x, 120 * y))
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def damage(self, damage, level, group):
        self.health -= damage
        if self.health <= 0:
            level[self.y][self.x] = Air(self.x, self.y)
            group.add(level[self.y][self.x])


class Air(Block):
    id = 1
    texture = Texture.air
    blastResistance = 0
    passable = True


class Grass(Block):
    id = 2
    texture = Texture.grass
    blastResistance = 10


class Dirt(Block):
    id = 3
    texture = Texture.dirt
    blastResistance = 0


class Stone(Block):
    id = 4
    texture = Texture.stone
    blastResistance = 30


class Iron(Block):
    id = 5
    texture = Texture.iron
    blastResistance = 70
