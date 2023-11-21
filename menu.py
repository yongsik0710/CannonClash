import pygame
from button import *
from levels import *
from stage import *
from shell import *


class Menu:
    def loop(self):
        pass


class MainMenu(Menu):
    def __init__(self, game):
        self.game = game
        font = pygame.font.Font(None, 50)
        self.stage_select = Button(game.screen, 790, 700, 400, 100, 5, font, "Stage Select")
        self.quit_button = Button(game.screen, 790, 820, 400, 100, 5, font, "Quit")
        self.loop()

    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.game.screen.fill((200, 200, 200))
            if self.stage_select.draw():
                StageSelect(self.game)
            if self.quit_button.draw():
                running = False

            pygame.display.update()
            self.game.clock.tick(self.game.FPS)


class StageSelect(Menu):
    def __init__(self, game):
        self.game = game
        font = pygame.font.Font(None, 50)
        self.stage_1 = Button(game.screen, 790, 700, 400, 100, 5, font, "Stage 1")
        self.loop()

    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.game.screen.fill((200, 200, 200))
            if self.stage_1.draw():
                running = False
                MissileGame(self.game, Stage(Levels.level_1, 1.0, 0.0))

            pygame.display.update()
            self.game.clock.tick(self.game.FPS)


class GameMenu(Menu):
    def __init__(self, game):
        self.game = game
        font = pygame.font.Font(None, 50)
        self.back_to_main_menu = Button(game.screen, 790, 700, 400, 100, 5, font, "Back to Main Menu")
        self.over = False
        self.loop()

    def loop(self):
        my_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        my_surface.fill((255, 255, 255, 100))
        self.game.screen.blit(my_surface, (0, 0))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if self.back_to_main_menu.draw():
                running = False
                self.over = True

            pygame.display.update()
            self.game.clock.tick(self.game.FPS)


class MissileGame:
    def __init__(self, game, stage):
        self.game = game
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
                        g = GameMenu(self.game)
                        if g.over:
                            running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.projectiles.add(Shell(self.stage, pygame.mouse.get_pos(), [0, 0]))

            self.game.screen.blit(self.background, (0, 0))
            self.blocks.draw(self.game.screen)
            self.projectiles.update()
            self.projectiles.draw(self.game.screen)

            for projectile in self.projectiles:
                if pygame.sprite.spritecollide(projectile, self.non_passable_blocks, False):
                    damagedBlocks = pygame.sprite.spritecollide(projectile, self.non_passable_blocks, False,
                                                                pygame.sprite.collide_circle)
                    projectile.explode(damagedBlocks, self.blocks)

            pygame.display.update()
            self.game.clock.tick(self.game.FPS)

