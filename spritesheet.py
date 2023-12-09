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
    def __init__(self, image, frame):
        self.sheet = load_png(image)
        self.frame = frame
        self.frame_width = self.sheet.get_width() / self.frame
        self.frame_height = self.sheet.get_height()

    def get_image(self, frame, scale):
        surf = pygame.surface.Surface((self.frame_width, self.frame_height)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        surf.blit(self.sheet, (-(self.frame_width * frame), 0))
        surf = pygame.transform.scale_by(surf, scale)

        return surf
