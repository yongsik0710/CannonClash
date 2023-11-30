import pygame
import random
from camera import *
from stage import *
from config import *


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
            player.cannon = player.cannon(self.camera_group, self.stage, level.spawn_points[i], [0, 0])

        self.background = pygame.image.load(level.background_image).convert()

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.camera_group.update()
        self.camera_group.custom_draw()
        # 화면 업데이트
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)

    def event_check(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.players[self.current_turn].cannon.move_right()

        if keys[pygame.K_LEFT]:
            self.players[self.current_turn].cannon.move_left()

        if keys[pygame.K_SPACE]:
            self.players[self.current_turn].power += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_display = self.game.game_menu

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.players[self.current_turn].shoot_shell()
                    self.players[self.current_turn].power = 0
                    self.next_turn()

    def next_turn(self):
        if self.current_turn + 1 < len(self.players):
            self.current_turn += 1
        else:
            self.current_turn = 0
