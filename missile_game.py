import pygame
from shell import *


class MissileGame:
    def __init__(self, screen, stage):
        self.screen = screen
        self.stage = stage

        self.background = pygame.image.load("Images/Backgrounds/forest.png").convert()

        self.blocks = pygame.sprite.Group()
        self.non_passable_blocks = pygame.sprite.Group()

        for y in range(18):
            for x in range(32):
                block = self.stage.level[y][x]
                self.blocks.add(block)
                if not block.passable: self.non_passable_blocks.add(block)

        self.projectiles = pygame.sprite.Group()
        self.state = "play"
        self.clicked = False

    def process(self):
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            self.projectiles.add(Shell(self.stage, pygame.mouse.get_pos(), [0, 0]))
        elif pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.screen.blit(self.background, (0, 0))
        self.blocks.draw(self.screen)
        self.projectiles.update()
        self.projectiles.draw(self.screen)

        for projectile in self.projectiles:
            if pygame.sprite.spritecollide(projectile, self.non_passable_blocks, False):
                damagedBlocks = pygame.sprite.spritecollide(projectile, self.non_passable_blocks, False,
                                                            pygame.sprite.collide_circle)
                projectile.explode(damagedBlocks, self.blocks)
