from config import *
import pygame
import os


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (20, 20))
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
    damage = 100
    explosion_radius = 50

    def __init__(self, stage, pos, vector):
        pygame.sprite.Sprite.__init__(self)
        self.damage = self.damage
        self.stage = stage
        self.vector = vector
        self.gravity = stage.gravity

        self.texture = load_png(self.texture)
        self.image, self.rect = self.texture
        self.rect = self.rect.move(pos)

        self.add(self.stage.projectiles)

        self.surf = pygame.surface.Surface((self.explosion_radius * 2, self.explosion_radius * 2)).convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.circle(self.surf, "#000000", (self.explosion_radius, self.explosion_radius), self.explosion_radius)
        self.explosion_mask = pygame.mask.from_surface(self.surf)
        # self.radius = self.explosion_radius - (self.rect.width * (2 ** (1 / 2)))
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def update(self):
        self.vector[1] += self.gravity / 5
        self.collide_check()
        self.rect = self.rect.move(self.vector)

    def collide_check(self):
        if pygame.sprite.spritecollide(self, self.stage.level_group, False, pygame.sprite.collide_mask):
            self.explode()

    def explode(self):
        # damage = self.damage * (((self.max_explosion_radius - distance) / 100) ** 2)
        pygame.mask.Mask.erase(self.stage.level.mask, self.explosion_mask, (self.rect.centerx - self.explosion_radius, self.rect.centery - self.explosion_radius))
        self.kill()
