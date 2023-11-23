import pygame
import copy
from blocks import *
from cannon import *


class Stage:
    def __init__(self, level, gravity, air_resistance):
        self.gravity = gravity
        self.air_resistance = air_resistance

        self.blocks = pygame.sprite.Group()
        self.passable_blocks = pygame.sprite.Group()
        self.non_passable_blocks = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.cannons = pygame.sprite.Group()

        self.cannon = Cannon(self, (100, 300), [0, 0])

        self.level = self.load_level(copy.deepcopy(level))  # deepcopy used

    def load_level(self, level):
        for y in range(36):
            for x in range(64):
                if level[y][x] == Vacuum.id:
                    level[y][x] = Vacuum(self, x, y)
                elif level[y][x] == Air.id:
                    level[y][x] = Air(self, x, y)
                elif level[y][x] == Grass.id:
                    level[y][x] = Grass(self, x, y)
                elif level[y][x] == Dirt.id:
                    level[y][x] = Dirt(self, x, y)
                elif level[y][x] == Stone.id:
                    level[y][x] = Stone(self, x, y)
                elif level[y][x] == Iron.id:
                    level[y][x] = Iron(self, x, y)
                else:
                    level[y][x] = Block(self, x, y)
        return level

    def update(self):
        pass

    def draw(self, surface):
        self.blocks.draw(surface)
        self.projectiles.update()
        self.cannons.update()
        self.projectiles.draw(surface)
        self.cannons.draw(surface)
