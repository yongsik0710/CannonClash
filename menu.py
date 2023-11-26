import pygame
from button import *
from textbox import *
from config import *
from missile_game import *
from cannon_select_ui import *


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
        self.game_start = Button(game.screen, 760, 700, 400, 100, 5, font, "Game Start")
        self.quit = Button(game.screen, 760, 820, 400, 100, 5, font, "Quit")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill((200, 200, 200))
        self.game_start.draw()
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

        if self.game_start.is_clicked():  # 스테이지 선택
            self.game.current_display = self.game.number_of_player_select

        if self.quit.is_clicked():  # 게임 종료
            self.stop = True


class NumberOfPlayerSelect(Menu):
    def __init__(self, game):
        super().__init__(game)
        font = pygame.font.Font(None, 50)
        title_font = pygame.font.Font(None, 80)
        self.number_of_player = 2
        self.title = TextBox(game.screen, 560, 240, 800, 150, title_font, '#808080', 'Select number of players')

        self.up = Button(game.screen, 1020, 540, 100, 100, 5, font, ">")
        self.player_count = TextBox(game.screen, 910, 540, 100, 100, font, '#475F77', str(self.number_of_player))
        self.down = Button(game.screen, 800, 540, 100, 100, 5, font, "<")

        self.next = Button(game.screen, 760, 700, 400, 100, 5, font, "Next")
        self.back = Button(game.screen, 760, 820, 400, 100, 5, font, "Back")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill((200, 200, 200))
        self.title.draw()
        if self.number_of_player < 6: self.up.draw()
        if self.number_of_player > 2: self.down.draw()
        self.player_count.draw()
        self.next.draw()
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

        if self.up.is_clicked():  # 플레이어 수 증가
            self.number_of_player += 1
            self.player_count.text = str(self.number_of_player)

        if self.down.is_clicked():  # 플레이어 수 감소
            self.number_of_player -= 1
            self.player_count.text = str(self.number_of_player)

        if self.next.is_clicked():  # 다음으로
            self.game.cannon_select = CannonSelect(self.game, self.number_of_player)
            self.game.current_display = self.game.cannon_select

        if self.back.is_clicked():  # 뒤로 가기
            self.game.current_display = self.game.main_menu


class CannonSelect(Menu):
    def __init__(self, game, number_of_player):
        super().__init__(game)
        self.players = [None for _ in range(number_of_player)]
        self.ui = []

        font = pygame.font.Font(None, 50)
        title_font = pygame.font.Font(None, 70)

        self.next = Button(game.screen, 760, 800, 400, 100, 5, font, "Next")
        self.back = Button(game.screen, 760, 920, 400, 100, 5, font, "Back")

        if number_of_player == 2:
            self.ui.append(CannonSelectUI(self.game.screen, 420, 200, title_font, font, "Player 1"))
            self.ui.append(CannonSelectUI(self.game.screen, 1120, 200, title_font, font, "Player 2"))

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill((200, 200, 200))
        self.next.draw()
        self.back.draw()
        for object in self.ui:
            object.draw()
        # 화면 업데이트
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_display = self.game.number_of_player_select

        if self.next.is_clicked():  # 다음으로
            self.game.current_display = self.game.stage_select

        if self.back.is_clicked():  # 뒤로 가기
            self.game.current_display = self.game.number_of_player_select


class StageSelect(Menu):
    def __init__(self, game):
        super().__init__(game)
        font = pygame.font.Font(None, 50)
        self.stage_1 = Button(game.screen, 760, 580, 400, 100, 5, font, "Stage 1")
        self.stage_2 = Button(game.screen, 760, 700, 400, 100, 5, font, "Stage 2")
        self.back = Button(game.screen, 760, 820, 400, 100, 5, font, "Back")

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
                    self.game.current_display = self.game.number_of_player_select

        if self.stage_1.is_clicked():  # 스테이지 1
            self.game.missile_game = MissileGame(self.game, [], Levels.test_level)
            self.game.current_display = self.game.missile_game

        if self.stage_2.is_clicked():  # 스테이지 2
            self.game.missile_game = MissileGame(self.game, [], Levels.level_2)
            self.game.current_display = self.game.missile_game

        if self.back.is_clicked():  # 메인 메뉴로 돌아가기
            self.game.current_display = self.game.number_of_player_select


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
