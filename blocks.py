from config import *
import pygame
import os


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (60, 60))
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
    texture = Texture.Blocks.none
    blastResistance = 0
    passable = False

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.x = x
        self.y = y

        self.texture = load_png(self.texture)
        self.image, self.rect = self.texture
        self.rect = self.rect.move((60 * x, 60 * y))
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def damage(self, damage, level, group):
        damage = int(damage * ((100 - self.blastResistance) / 100))
        self.health -= damage
        if self.health <= 0:
            level[self.y][self.x] = Air(self.x, self.y)
            group.add(level[self.y][self.x])


class Air(Block):
    id = 1
    texture = Texture.Blocks.air
    blastResistance = 0
    passable = True


class Grass(Block):
    id = 2
    texture = Texture.Blocks.grass
    blastResistance = 10


class Dirt(Block):
    id = 3
    texture = Texture.Blocks.dirt
    blastResistance = 0


class Stone(Block):
    id = 4
    texture = Texture.Blocks.stone
    blastResistance = 30


class Iron(Block):
    id = 5
    texture = Texture.Blocks.iron
    blastResistance = 70
