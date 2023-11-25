import pygame
import copy
from cannon import *
from levels import *


class Stage:
    def __init__(self, level, gravity, air_resistance):
        self.level_group = pygame.sprite.Group()
        self.level = Level(self.level_group, level, (0, 0))
        self.gravity = gravity
        self.air_resistance = air_resistance

        self.projectiles = pygame.sprite.Group()
        self.cannons = pygame.sprite.Group()

        self.cannon = Cannon(self, (100, 300), [0, 0])

    def update(self):
        pass

    def draw(self, surface):
        self.level_group.update()
        self.level_group.draw(surface)
        self.projectiles.draw(surface)
        self.projectiles.update()
        self.cannons.update()
        self.cannons.draw(surface)
