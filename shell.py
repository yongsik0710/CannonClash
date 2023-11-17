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


class Shell(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, stage, pos, vector):
        pygame.sprite.Sprite.__init__(self)
        self.damage = 80
        self.radius = 60
        self.stage = stage
        self.vector = vector
        self.gravity = stage.gravity
        self.image, self.rect = load_png('ball.png')
        self.rect = self.rect.move(pos)
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
            block.damage(120, self.stage.level, group)
            print(pygame.math.Vector2(self.rect.center).distance_to(block.rect.center))
        print("펑!")
        self.kill()
