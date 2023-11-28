import pygame
import random
from camera import *
from stage import *


class MissileGame:
    def __init__(self, game, players, level):
        self.game = game
        self.stop = False
        self.current_turn = 0
        self.camera_group = CameraGroup()
        self.players = players
        self.stage = Stage(self.camera_group, level)

        random.shuffle(level.spawn_points)
        for i, player in enumerate(players):
            player.missile_game = self
            player.cannon = player.cannon(self.camera_group, self.stage, level.spawn_points[i], [0, 0])
        self.test_image = self.players[0].cannon.image

        self.background = pygame.image.load(level.background_image).convert()

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.camera_group.update()
        self.camera_group.custom_draw()

        surf = pygame.surface.Surface((32, 32)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        surf.blit(self.stage.image, (-(self.players[0].cannon.collide_pos[0] - 16), -(self.players[0].cannon.collide_pos[1])))
        mask = pygame.mask.from_surface(surf)
        a = mask.outline()
        b = []
        for x in range(32):
            for y in range(32):
                if mask.get_at((x, y)):
                    b.append((x, y))
                    break

        c = [0, 0]
        for i in range(len(b)):
            c[0] += b[i][0] - b[0][0]
            c[1] += b[i][1] - b[0][1]

        try:
            pygame.draw.line(surf, (255, 255, 0), b[0], (b[0][0] + c[0], b[0][1] + c[1]), 1)
            angle = pygame.Vector2(self.players[0].cannon.rect.x + 38 - self.players[0].cannon.collide_pos[0], self.players[0].cannon.rect.y + 75 - self.players[0].cannon.collide_pos[1])
            angle = angle.rotate(90)
            angle = angle.angle_to((0, 0))
            test_surf = pygame.transform.rotate(self.test_image, angle)
        except:
            pass
        # self.game.screen.blit(test_surf, (200, 100))
        # self.game.screen.blit(surf, (100, 100))
        # 화면 업데이트
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)

    def event_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.players[0].cannon.move_right()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_display = self.game.game_menu

            # 플레이어 행동
            self.players[self.current_turn].process(event)

    def next_turn(self):
        if self.current_turn + 1 < len(self.players):
            self.current_turn += 1
        else:
            self.current_turn = 0
