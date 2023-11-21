import pygame
from shell import *
from menu import *


class MissileGame:
    def __init__(self, game, stage):
        self.game = game
        self.screen = game.screen
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
        self.loop()

    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        GameMenu(self.game)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.projectiles.add(Shell(self.stage, pygame.mouse.get_pos(), [0, 0]))

            self.screen.blit(self.background, (0, 0))
            self.blocks.draw(self.screen)
            self.projectiles.update()
            self.projectiles.draw(self.screen)

            for projectile in self.projectiles:
                if pygame.sprite.spritecollide(projectile, self.non_passable_blocks, False):
                    damagedBlocks = pygame.sprite.spritecollide(projectile, self.non_passable_blocks, False,
                                                                pygame.sprite.collide_circle)
                    projectile.explode(damagedBlocks, self.blocks)

            pygame.display.update()
            self.game.clock.tick(self.game.FPS)
