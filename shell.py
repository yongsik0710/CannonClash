from config import *
import pygame
import os


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
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


class Shell(pygame.sprite.Sprite):
    texture = Texture.Shells.basic
    damage = 150
    max_explosion_radius = 120

    def __init__(self, stage, pos, vector):
        pygame.sprite.Sprite.__init__(self)
        self.damage = self.damage
        self.stage = stage
        self.vector = vector
        self.gravity = stage.gravity

        self.texture = load_png(self.texture)
        self.image, self.rect = self.texture
        self.rect = self.rect.move(pos)

        self.radius = self.max_explosion_radius - (self.rect.width * (2 ** (1 / 2)))
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def update(self):
        self.vector[1] += self.gravity / 5
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos

    def calcnewpos(self, rect, vector):
        return rect.move(vector)

    def explode(self, blocks, group):
        for block in blocks:
            distance = pygame.math.Vector2(self.rect.center).distance_to(block.rect.center)
            damage = self.damage * (((self.max_explosion_radius - distance) / 100) ** 2)
            print(distance, damage)
            block.damage(damage, self.stage.level, group)
        print("펑!")
        self.kill()
