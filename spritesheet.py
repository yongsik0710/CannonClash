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
    return image


class SpriteSheet:
    def __init__(self, image, frame, scale):
        self.sprites = []
        image = load_png(image)
        frame_width = image.get_width() / frame
        frame_height = image.get_height()

        for i in range(frame):
            surf = pygame.surface.Surface((frame_width, frame_height)).convert_alpha()
            surf.fill((0, 0, 0, 0))
            surf.blit(image, (-(frame_width * i), 0))
            surf = pygame.transform.scale_by(surf, scale)
            self.sprites.append(surf)
