import pygame
import random
from camera import *
from stage import *


class MissileGame:
    def __init__(self, game, players, level):
        self.game = game
        self.stop = False
        self.turn = 0
        self.camera_group = CameraGroup()
        self.players = players
        self.stage = Stage(self.camera_group, level)

        random.shuffle(level.spawn_points)
        for i, player in enumerate(players):
            player.cannon = player.cannon(self.camera_group, self.stage, level.spawn_points[i], [0, 0])

        self.background = pygame.image.load(level.background_image).convert()

    def loop(self):
        # 플레이어 행동
        self.players[self.turn].process()
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.camera_group.update()
        self.camera_group.custom_draw()
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
                    pass
                    # Shell(self.stage.camera_group, self.stage, pygame.mouse.get_pos(), [0, 0])
