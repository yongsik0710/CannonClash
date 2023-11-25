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


class Level(pygame.sprite.Sprite):
    def __init__(self, group, level, pos):
        pygame.sprite.Sprite.__init__(self, group)

        self.level = load_png(level)
        self.image, self.rect = self.level
        self.rect = self.rect.move(pos)

        self.mask = pygame.mask.from_surface(self.image)

        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def update(self):
        self.image = self.mask.to_surface(setsurface=self.image, unsetcolor=(255, 0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
