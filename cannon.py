from config import *
import pygame
import os


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (80, 80))
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

    def __init__(self, group, stage, pos, vector):
        pygame.sprite.Sprite.__init__(self, group)
        self.stage = stage
        self.vector = vector
        self.gravity = stage.gravity

        self.texture = load_png(self.texture)
        self.image, self.rect = self.texture
        self.rect = self.rect.move(pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.add(self.stage.cannons)
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def update(self):
        self.vector[1] += self.gravity / 5
        self.collide_check()
        self.rect = self.rect.move(self.vector)

    def collide_check(self):
        if pygame.sprite.spritecollide(self, self.stage.level_group, False, pygame.sprite.collide_mask):
            self.vector = [0, 0]

    def shoot_shell(self):
        pass
