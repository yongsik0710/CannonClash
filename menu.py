import pygame
from button import *
from shell import *
from stage import *
from levels import *


class Menu:
    def __init__(self, game):
        self.game = game
        self.stop = False

    def loop(self):
        pass

    def event_check(self):
        pass


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        font = pygame.font.Font(None, 50)
        self.stage_select = Button(game.screen, 790, 700, 400, 100, 5, font, "Stage Select")
        self.quit = Button(game.screen, 790, 820, 400, 100, 5, font, "Quit")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill((200, 200, 200))
        self.stage_select.draw()
        self.quit.draw()
        # 화면 업데이트
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop = True

        if self.stage_select.is_clicked():  # 스테이지 선택
            self.game.current_display = self.game.stage_select

        if self.quit.is_clicked():  # 게임 종료
            self.stop = True


class StageSelect(Menu):
    def __init__(self, game):
        super().__init__(game)
        font = pygame.font.Font(None, 50)
        self.stage_1 = Button(game.screen, 790, 580, 400, 100, 5, font, "Stage 1")
        self.stage_2 = Button(game.screen, 790, 700, 400, 100, 5, font, "Stage 2")
        self.back = Button(game.screen, 790, 820, 400, 100, 5, font, "Back")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill((200, 200, 200))
        self.stage_1.draw()
        self.stage_2.draw()
        self.back.draw()
        # 화면 업데이트
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_display = self.game.main_menu

        if self.stage_1.is_clicked():  # 스테이지 1
            self.game.missile_game = MissileGame(self.game, Stage(Levels.level_1, 1.0, 0.0))
            self.game.current_display = self.game.missile_game

        if self.stage_2.is_clicked():  # 스테이지 2
            self.game.missile_game = MissileGame(self.game, Stage(Levels.level_2, 1.0, 0.0))
            self.game.current_display = self.game.missile_game

        if self.back.is_clicked():  # 메인 메뉴로 돌아가기
            self.game.current_display = self.game.main_menu


class GameMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        font = pygame.font.Font(None, 50)
        self.resume = Button(game.screen, 790, 580, 400, 100, 5, font, "Resume")
        self.back_to_main_menu = Button(game.screen, 790, 700, 400, 100, 5, font, "Back to Main Menu")

        # my_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        # my_surface.fill((255, 255, 255, 100))
        # self.game.screen.blit(my_surface, (0, 0))

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.resume.draw()
        self.back_to_main_menu.draw()
        # 화면 업데이트
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_display = self.game.missile_game

        if self.resume.is_clicked():  # 게임으로
            self.game.current_display = self.game.missile_game

        if self.back_to_main_menu.is_clicked():  # 메인 메뉴로 이동
            self.game.current_display = self.game.main_menu


class MissileGame(Menu):
    def __init__(self, game, stage):
        super().__init__(game)
        self.stage = stage

        self.background = pygame.image.load("Images/Backgrounds/forest.png").convert()

        self.blocks = pygame.sprite.Group()
        self.non_passable_blocks = pygame.sprite.Group()

        for y in range(18):
            for x in range(32):
                block = self.stage.level[y][x]
                self.blocks.add(block)
                if not block.passable:
                    self.non_passable_blocks.add(block)

        self.projectiles = pygame.sprite.Group()

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.blit(self.background, (0, 0))
        self.blocks.draw(self.game.screen)
        self.projectiles.update()
        self.projectiles.draw(self.game.screen)
        # 충돌 감지
        self.collide_detect()
        # 화면 업데이트
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_display = self.game.game_menu

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.projectiles.add(Shell(self.stage, pygame.mouse.get_pos(), [0, 0]))

    def collide_detect(self):
        for projectile in self.projectiles:
            if pygame.sprite.spritecollide(projectile, self.non_passable_blocks, False):
                damaged_blocks = pygame.sprite.spritecollide(projectile,
                                                             self.non_passable_blocks, False,
                                                             pygame.sprite.collide_circle)
                projectile.explode(damaged_blocks, self.blocks)
