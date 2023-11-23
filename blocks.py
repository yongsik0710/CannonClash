from config import *
import pygame
import os


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (30, 30))
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
    blast_resistance = 0
    passable = False

    def __init__(self, stage, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.stage = stage
        self.x = x
        self.y = y

        self.health = 100

        self.texture = load_png(self.texture)
        self.image, self.rect = self.texture
        self.rect = self.rect.move((30 * x, 30 * y))

        if self.passable:
            self.add(self.stage.passable_blocks, stage.blocks)
        else:
            self.add(self.stage.non_passable_blocks, stage.blocks)
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def damage(self, damage):
        damage = int(damage * ((100 - self.blast_resistance) / 100))
        self.health -= damage
        if self.health <= 0:
            self.stage.level[self.y][self.x] = Vacuum(self.stage, self.x, self.y)
            self.kill()


class Vacuum(Block):
    id = 1
    texture = Texture.Blocks.air_transparent
    blast_resistance = 0
    passable = True


class Air(Block):
    id = 2
    texture = Texture.Blocks.air_transparent
    blast_resistance = 0
    passable = True


class Grass(Block):
    id = 3
    texture = Texture.Blocks.grass
    blast_resistance = 10


class Dirt(Block):
    id = 4
    texture = Texture.Blocks.dirt
    blast_resistance = 0


class Stone(Block):
    id = 5
    texture = Texture.Blocks.stone
    blast_resistance = 30


class Iron(Block):
    id = 6
    texture = Texture.Blocks.iron
    blast_resistance = 70
