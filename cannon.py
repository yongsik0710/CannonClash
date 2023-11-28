from shell import *
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
    return image


class Cannon(pygame.sprite.Sprite):
    name = None
    barrel_texture = None
    wheel_texture = None
    shell = None

    def __init__(self, group, stage, pos, vector):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.health = 1000
        self.stage = stage
        self.vector = pygame.math.Vector2(vector)
        self.gravity = stage.gravity

        surf = pygame.surface.Surface((100, 100)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        surf.blit(load_png(self.barrel_texture), (0, 0))
        surf.blit(load_png(self.wheel_texture), (0, 0))
        self.image, self.rect = surf, surf.get_rect()
        self.rect = self.rect.move(pos)
        self.mask = pygame.mask.from_surface(load_png(self.wheel_texture))

        self.collide_pos = (0, 0)
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def update(self):
        self.vector.y += self.gravity / 10
        self.collide_check()
        self.rect = self.rect.move(self.vector)

    def collide_check(self):
        if pygame.sprite.collide_mask(self, self.stage):
            self.collide_pos = self.mask.overlap(self.stage.mask, (-self.rect.x, -self.rect.y))
            self.collide_pos = (self.collide_pos[0] + self.rect.x, self.collide_pos[1] + self.rect.y)
            self.vector.y = -1

    def shoot_shell(self, vector):
        self.shell(self.camera, self.stage, (self.rect.centerx, self.rect.centery - 20), vector)

    def move_right(self):
        self.rect = self.rect.move(1, 0)


class BasicCannon(Cannon):
    name = "Basic"
    barrel_texture = TexturePath.Cannon.Barrel.barrel_1
    wheel_texture = TexturePath.Cannon.Wheel.wheel_1
    shell = BasicShell


class TestCannon(Cannon):
    name = "Test"
    barrel_texture = TexturePath.Cannon.Barrel.barrel_2
    wheel_texture = TexturePath.Cannon.Wheel.wheel_2
    shell = Shell


CANNONS = {
    1: BasicCannon,
    2: TestCannon
}