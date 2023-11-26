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


class Stage(pygame.sprite.Sprite):
    def __init__(self, group, level):
        pygame.sprite.Sprite.__init__(self, group)
        self.image, self.rect = load_png(level["level_image"])
        self.mask = pygame.mask.from_surface(self.image)

        self.gravity = level["gravity"]
        self.air_resistance = level["air_resistance"]

    def custom_update(self):
        self.image = self.mask.to_surface(setsurface=self.image, unsetcolor=(255, 0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
