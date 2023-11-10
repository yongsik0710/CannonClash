from config import *
import pygame


class Block(pygame.sprite.Sprite):
    blastResistance = 0
    passable = False
    texture = ""

    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.image, self.rect = load_png('iron.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector


class Air(Block):
    texture = Texture.air
    blastResistance = 0
    passable = True


class Grass(Block):
    texture = Texture.grass
    blastResistance = 0


class Dirt(Block):
    texture = Texture.dirt
    blastResistance = 0


class Stone(Block):
    texture = Texture.stone
    blastResistance = 30


class Iron(Block):
    texture = Texture.iron
    blastResistance = 70
