import pygame
import random
from camera import *
from stage import *
from config import *
from button import *
from textbox import *


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (240, 240))
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image


class MissileGame:
    def __init__(self, game, players, level):
        self.game = game
        self.stop = False
        self.current_turn = 0
        self.camera_group = CameraGroup()
        self.cannon_group = pygame.sprite.Group()
        self.players = players
        self.stage = Stage(self.camera_group, level)

        random.shuffle(level.spawn_points)
        for i, player in enumerate(players):
            player.missile_game = self
            player.cannon = player.cannon([self.camera_group, self.cannon_group], self.stage, level.spawn_points[i], [0, 0], player)
            player.init_player_ui()
        self.players[self.current_turn].turn = True

        self.background = pygame.image.load(level.background_image).convert()

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.camera_group.update()
        self.camera_group.custom_draw()
        self.players[self.current_turn].draw_player_ui()
        # 화면 업데이트
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)

    def event_check(self):
        keys = pygame.key.get_pressed()

        if self.players[self.current_turn].turn:

            if keys[pygame.K_RIGHT]:
                self.players[self.current_turn].cannon.move_right()

            if keys[pygame.K_LEFT]:
                self.players[self.current_turn].cannon.move_left()

            if keys[pygame.K_SPACE]:
                if self.players[self.current_turn].power < self.players[self.current_turn].max_power:
                    self.players[self.current_turn].power += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_display = self.game.game_menu

            if self.players[self.current_turn].turn:

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.players[self.current_turn].shoot_shell()

    def next_turn(self):
        # 게임 종료 테스트
        self.is_game_end()

        if self.current_turn + 1 < len(self.players):
            self.current_turn += 1
        else:
            self.current_turn = 0

        if not self.players[self.current_turn].is_death:
            self.camera_group.center_target_camera_align(self.players[self.current_turn].cannon)
            self.players[self.current_turn].turn = True
        else:
            self.players[self.current_turn].skip()

    def is_game_end(self):
        if len([player for player in self.players if not player.is_death]) <= 1:
            self.game_end(self.players[0])

    def game_end(self, winner):
        self.game.current_display = GameEnd(self.game, winner)


class GameEnd:
    def __init__(self, game, winner):
        self.game = game
        self.stop = False
        self.winner = winner
        title_font = pygame.font.Font(None, 80)
        font = pygame.font.Font(None, 50)

        self.winner_text = TextBox(game.screen, 560, 300, 800, 150, title_font, "#808080", f"{self.winner.name} win this game!!")
        self.back_to_main_menu = Button(game.screen, 760, 700, 400, 100, 5, font, "Back to Main Menu")

        # my_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        # my_surface.fill((255, 255, 255, 100))
        # self.game.screen.blit(my_surface, (0, 0))

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill("#e0e0e0")
        self.winner_text.draw()
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
                    self.game.current_display = self.game.main_menu

        if self.back_to_main_menu.is_clicked():  # 메인 메뉴로 이동
            self.game.current_display = self.game.main_menu
