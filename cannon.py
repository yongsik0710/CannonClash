from config import *
import pygame
import os


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (100, 100))
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()


class Cannon(pygame.sprite.Sprite):
    texture = Texture.Cannon.basic

    def __init__(self, stage, pos, vector):
        pygame.sprite.Sprite.__init__(self)
        self.stage = stage
        self.vector = vector
        self.gravity = stage.gravity

        self.texture = load_png(self.texture)
        self.image, self.rect = self.texture
        self.rect = self.rect.move(pos)

        self.add(self.stage.cannons)
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def update(self):
        self.vector[1] += self.gravity / 5
        self.collide_check()
        self.rect = self.rect.move(self.vector)

    def collide_check(self):
        if pygame.sprite.spritecollide(self, self.stage.non_passable_blocks, False):
            self.vector = [0, 0]

    def explode(self, blocks):
        for block in blocks:
            distance = pygame.math.Vector2(self.rect.center).distance_to(block.rect.center)
            damage = self.damage * (((self.max_explosion_radius - distance) / 100) ** 2)
            print(distance, damage)
            block.damage(damage)
        print("펑!")
        self.kill()
