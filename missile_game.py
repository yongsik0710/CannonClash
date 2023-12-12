import pygame

from camera import *
from stage import *
from ui_component.button import *
from ui_component.textbox import *


class MissileGame:
    def __init__(self, game, players, level):
        self.game = game
        self.stop = False
        self.current_turn = 0
        self.background = pygame.image.load(level.background_image).convert()
        self.camera_group = CameraGroup(self.background)
        self.cannon_group = pygame.sprite.Group()
        self.players = players
        self.stage = Stage(self.camera_group, level)

        random.shuffle(level.spawn_points)
        for i, player in enumerate(players):
            player.missile_game = self
            player.cannon = player.cannon([self.camera_group, self.cannon_group], self.stage, level.spawn_points[i], [0, 0], player)
            player.cannon.direction = random.choice(["right", "left"])
            player.init_player_ui()
        self.players[self.current_turn].turn = True
        self.camera_group.center_target_camera_align(self.players[self.current_turn].cannon)

        self.game_menu_on = False

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        if not self.game_menu_on:
            self.camera_group.update()
            self.camera_group.custom_draw()
            for player in self.players:
                if not player.is_death:
                    player.cannon.draw_cannon_ui()
            self.players[self.current_turn].draw_player_ui()
            # 화면 업데이트
            pygame.display.update()
            self.game.clock.tick(self.game.FPS)
        else:
            self.game_menu_pop()
            self.game_menu_on = False

    def event_check(self):
        keys = pygame.key.get_pressed()

        if self.players[self.current_turn].turn:

            if keys[pygame.K_SPACE]:
                self.players[self.current_turn].cannon.barrel_move_sound.sound.stop()
                self.players[self.current_turn].cannon.move_sound.sound.stop()
                if self.players[self.current_turn].power < self.players[self.current_turn].max_power:
                    self.players[self.current_turn].power += 1.3
            else:
                if keys[pygame.K_RIGHT]:
                    self.players[self.current_turn].cannon.move_right()

                if keys[pygame.K_LEFT]:
                    self.players[self.current_turn].cannon.move_left()

                if keys[pygame.K_UP]:
                    self.players[self.current_turn].cannon.angle_up()

                if keys[pygame.K_DOWN]:
                    self.players[self.current_turn].cannon.angle_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_menu_on = True

                if event.key == pygame.K_LCTRL:
                    self.camera_group.center_target_camera_align(self.players[self.current_turn].cannon)

            if self.players[self.current_turn].turn:

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.players[self.current_turn].shoot_shell()

                    if event.key == pygame.K_RIGHT:
                        self.players[self.current_turn].cannon.move_sound.sound.stop()

                    if event.key == pygame.K_LEFT:
                        self.players[self.current_turn].cannon.move_sound.sound.stop()

                    if event.key == pygame.K_UP:
                        self.players[self.current_turn].cannon.barrel_move_sound.sound.stop()

                    if event.key == pygame.K_DOWN:
                        self.players[self.current_turn].cannon.barrel_move_sound.sound.stop()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print(pygame.mouse.get_pos() + self.camera_group.offset)

                if not keys[pygame.K_SPACE]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            self.players[self.current_turn].cannon.move_sound.sound.play(-1)

                        if event.key == pygame.K_LEFT:
                            self.players[self.current_turn].cannon.move_sound.sound.play(-1)

                        if event.key == pygame.K_UP:
                            self.players[self.current_turn].cannon.barrel_move_sound.sound.play(-1)

                        if event.key == pygame.K_DOWN:
                            self.players[self.current_turn].cannon.barrel_move_sound.sound.play(-1)

    def game_menu_pop(self):
        pygame.mixer.pause()
        self.game.current_display = self.game.game_menu
        surf = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        surf.fill((255, 255, 255, 160))
        self.game.screen.blit(surf, (0, 0))

    def next_turn(self):
        # 게임 종료 테스트
        self.is_game_end()
        self.wind_change()
        self.players[self.current_turn].cannon.mobility = self.players[self.current_turn].cannon.max_mobility

        if self.current_turn + 1 < len(self.players):
            self.current_turn += 1
        else:
            self.current_turn = 0

        if self.players[self.current_turn].cannon.fire_turn > 0:
            self.players[self.current_turn].cannon.damage(random.randint(30, 70), is_fire=True)
            self.players[self.current_turn].cannon.fire_turn -= 1
            if self.players[self.current_turn].cannon.fire_turn <= 0:
                if self.players[self.current_turn].cannon.fire_effect is not None:
                    self.players[self.current_turn].cannon.fire_effect.kill()
                    self.players[self.current_turn].cannon.fire_effect = None

        if not self.players[self.current_turn].is_death:
            self.camera_group.center_target_camera_align(self.players[self.current_turn].cannon)
            self.players[self.current_turn].turn = True
        else:
            self.players[self.current_turn].skip()

    def wind_change(self):
        self.stage.wind += random.randint(-25, 25)
        if self.stage.wind > 100:
            self.stage.wind = 100
        elif self.stage.wind < -100:
            self.stage.wind = -100

    def is_game_end(self):
        alive_players = [player for player in self.players if not player.is_death]
        if len(alive_players) <= 1:
            self.game_end(alive_players[0])

    def game_end(self, winner):
        pygame.mixer.stop()
        self.game.current_display = GameEnd(self.game, winner)


class GameEnd:
    def __init__(self, game, winner):
        self.game = game
        self.stop = False
        self.winner = winner

        self.winner_text = TextBox(game.screen, 510, 300, 900, 150, 70, f"{self.winner.name} 님이 승리했습니다!")
        self.back_to_main_menu = Button(game.screen, 760, 700, 400, 100, 5, 40, "메인 메뉴로 돌아가기")

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
                if event.key == pygame.K_ESCAPE:  # 메인 메뉴로 이동
                    pygame.mixer_music.load(Resources.Sounds.Music.lobby)
                    pygame.mixer_music.play()
                    self.game.current_display = self.game.main_menu

        if self.back_to_main_menu.is_clicked():  # 메인 메뉴로 이동
            pygame.mixer_music.load(Resources.Sounds.Music.lobby)
            pygame.mixer_music.play()
            self.game.current_display = self.game.main_menu
