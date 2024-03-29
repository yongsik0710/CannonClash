from missile_game import *
from cannon_selector import *
from ui_component.stage_button import *
from player import *
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
        self.title_image = load_png(Resources.Texture.Util.title)
        self.title_image = pygame.transform.scale_by(self.title_image, 0.6)
        self.background_image = load_png(Resources.Texture.Levels.Level2.background_image)
        self.background_image = pygame.transform.scale(self.background_image, (1920, 1080))
        self.game_start = Button(game.screen, 760, 510, 400, 100, 5, 40, "게임 시작")
        self.game_explain = Button(game.screen, 760, 630, 400, 100, 5, 40, "게임 설명")
        self.options = Button(game.screen, 760, 750, 400, 100, 5, 40, "설정")
        self.quit = Button(game.screen, 760, 900, 400, 100, 5, 40, "게임 종료")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill("#e0e0e0")
        self.game.screen.blit(self.background_image, (0, 0))
        self.game.screen.blit(self.title_image, (384, 30))
        self.game_start.draw()
        self.game_explain.draw()
        self.options.draw()
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

        if self.game_start.is_clicked():  # 플레이어 수 선택
            self.game.current_display = self.game.number_of_player_select

        if self.game_explain.is_clicked():  # 게임 설명 화면
            self.game.current_display = self.game.game_explain

        if self.options.is_clicked():  # 설정 화면
            self.game.current_display = self.game.option

        if self.quit.is_clicked():  # 게임 종료
            self.stop = True


class GameExplain(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.current_page = 1
        self.pages = []
        self.pages.append(load_png(Resources.Texture.GameExplain.page_1))
        self.pages.append(load_png(Resources.Texture.GameExplain.page_2))
        self.pages.append(load_png(Resources.Texture.GameExplain.page_3))
        self.pages.append(load_png(Resources.Texture.GameExplain.page_4))
        self.pages.append(load_png(Resources.Texture.GameExplain.page_5))

        self.next = Button(game.screen, 1670, 950, 200, 100, 5, 40, "다음 >", border_ratio=5)
        self.prev = Button(game.screen, 50, 950, 200, 100, 5, 40, "< 이전", border_ratio=5)
        self.back_to_main_menu = Button(game.screen, 760, 950, 400, 100, 5, 40, "메인 메뉴로 돌아가기")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill("#e0e0e0")
        self.game.screen.blit(self.pages[self.current_page - 1], (192, 50))
        if self.current_page < 5: self.next.draw()
        if self.current_page > 1: self.prev.draw()
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
                    self.current_page = 1
                    self.game.current_display = self.game.main_menu

        if self.next.is_clicked():  # 다음 페이지
            self.current_page += 1

        if self.prev.is_clicked():  # 이전 페이지
            self.current_page -= 1

        if self.back_to_main_menu.is_clicked():  # 메인 메뉴로
            self.current_page = 1
            self.game.current_display = self.game.main_menu


class Option(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.volume = option["audio"]["volume"]
        self.keyboard_camera = option["util"]["keyboard_camera"]
        self.mouse_camera = option["util"]["mouse_camera"]
        self.title = TextBox(game.screen, 760, 100, 400, 100, 65, text='설정')

        self.volume_setting = TextBox(game.screen, 660, 250, 200, 100, 50, text='볼륨')
        self.keyboard_camera_setting = TextBox(game.screen, 410, 400, 500, 100, 50, text='키보드로 카메라 이동')
        self.mouse_camera_setting = TextBox(game.screen, 410, 550, 500, 100, 50, text='마우스로 카메라 이동')

        self.volume_display = TextBox(game.screen, 1050, 250, 100, 100, 40, text=str(self.volume), border_ratio=2)
        self.volume_up = Button(game.screen, 1170, 260, 80, 80, 4, 35, ">", border_ratio=2)
        self.volume_down = Button(game.screen, 950, 260, 80, 80, 4, 35, "<", border_ratio=2)
        self.volume_up_off = TextBox(game.screen, 1170, 258, 80, 80, 35, ">", background_color="#354b5e", border_ratio=2)
        self.volume_down_off = TextBox(game.screen, 950, 258, 80, 80, 35, "<", background_color="#354b5e", border_ratio=2)

        if self.keyboard_camera:
            self.keyboard_camera_check = Button(game.screen, 1050, 400, 100, 100, 4, 35, "O",
                                                top_color="#66a158", bottom_color="#528246", change_color="#3d5e35", border_ratio=2)
        else:
            self.keyboard_camera_check = Button(game.screen, 1050, 400, 100, 100, 4, 35, "X",
                                                top_color="#a15858", bottom_color="#824646", change_color="#5e3535",
                                                border_ratio=2)
        if self.mouse_camera:
            self.mouse_camera_check = Button(game.screen, 1050, 550, 100, 100, 4, 35, "O",
                                             top_color="#66a158", bottom_color="#528246", change_color="#3d5e35", border_ratio=2)
        else:
            self.mouse_camera_check = Button(game.screen, 1050, 550, 100, 100, 4, 35, "X",
                                             top_color="#a15858", bottom_color="#824646", change_color="#5e3535", border_ratio=2)

        self.apply = Button(game.screen, 760, 750, 400, 100, 5, 40, "적용")
        self.back = Button(game.screen, 760, 870, 400, 100, 5, 40, "뒤로")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill("#e0e0e0")
        self.title.draw()
        self.volume_setting.draw()
        self.keyboard_camera_setting.draw()
        self.mouse_camera_setting.draw()
        if self.volume < 10: self.volume_up.draw()
        else: self.volume_up_off.draw()
        if self.volume > 0: self.volume_down.draw()
        else: self.volume_down_off.draw()
        self.volume_display.draw()
        self.keyboard_camera_check.draw()
        self.mouse_camera_check.draw()
        self.apply.draw()
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

        if self.volume_up.is_clicked():  # 볼륨 증가
            self.volume += 1
            self.volume_display.text_update(str(self.volume))

        if self.volume_down.is_clicked():  # 볼륨 감소
            self.volume -= 1
            self.volume_display.text_update(str(self.volume))

        if self.keyboard_camera_check.is_clicked():  # 키보드로 카메라 이동
            if self.keyboard_camera:
                self.keyboard_camera = False
                self.keyboard_camera_check.text_update("X")
                self.keyboard_camera_check.top_original_color = "#a15858"
                self.keyboard_camera_check.bottom_color = "#824646"
                self.keyboard_camera_check.change_color = "#5e3535"
            else:
                self.keyboard_camera = True
                self.keyboard_camera_check.text_update("O")
                self.keyboard_camera_check.top_original_color = "#66a158"
                self.keyboard_camera_check.bottom_color = "#528246"
                self.keyboard_camera_check.change_color = "#3d5e35"

        if self.mouse_camera_check.is_clicked():  # 키보드로 카메라 이동
            if self.mouse_camera:
                self.mouse_camera = False
                self.mouse_camera_check.text_update("X")
                self.mouse_camera_check.top_original_color = "#a15858"
                self.mouse_camera_check.bottom_color = "#824646"
                self.mouse_camera_check.change_color = "#5e3535"
            else:
                self.mouse_camera = True
                self.mouse_camera_check.text_update("O")
                self.mouse_camera_check.top_original_color = "#66a158"
                self.mouse_camera_check.bottom_color = "#528246"
                self.mouse_camera_check.change_color = "#3d5e35"

        if self.apply.is_clicked():  # 적용
            option["audio"]["volume"] = self.volume
            option["util"]["keyboard_camera"] = self.keyboard_camera
            option["util"]["mouse_camera"] = self.mouse_camera
            all_sounds.set_volume(option["audio"]["volume"] / 10)
            with open(option_file, 'w') as option_data:
                json_data = json.dumps(option, indent="\t")
                option_data.write(json_data)

        if self.back.is_clicked():  # 뒤로 가기
            self.volume = option["audio"]["volume"]
            self.volume_display.text_update(str(self.volume))
            self.game.current_display = self.game.main_menu


class NumberOfPlayerSelect(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.number_of_player = 2
        self.title = TextBox(game.screen, 460, 200, 1000, 150, 65, text='참가할 플레이어 수를 정해주세요')

        self.player_count = TextBox(game.screen, 910, 500, 100, 100, 40, text=str(self.number_of_player), border_ratio=2)
        self.up = Button(game.screen, 1030, 510, 80, 80, 4, 35, ">", border_ratio=2)
        self.down = Button(game.screen, 810, 510, 80, 80, 4, 35, "<", border_ratio=2)
        self.up_off = TextBox(game.screen, 1030, 508, 80, 80, 35, ">", background_color="#354b5e", border_ratio=2)
        self.down_off = TextBox(game.screen, 810, 508, 80, 80, 35, "<", background_color="#354b5e", border_ratio=2)

        self.next = Button(game.screen, 760, 750, 400, 100, 5, 40, "다음")
        self.back = Button(game.screen, 760, 870, 400, 100, 5, 40, "뒤로")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill("#e0e0e0")
        self.title.draw()
        if self.number_of_player < 6: self.up.draw()
        else: self.up_off.draw()
        if self.number_of_player > 2: self.down.draw()
        else: self.down_off.draw()
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
            self.player_count.text_update(str(self.number_of_player))

        if self.down.is_clicked():  # 플레이어 수 감소
            self.number_of_player -= 1
            self.player_count.text_update(str(self.number_of_player))

        if self.next.is_clicked():  # 다음으로
            self.game.cannon_select = CannonSelect(self.game, self.number_of_player)
            self.game.current_display = self.game.cannon_select

        if self.back.is_clicked():  # 뒤로 가기
            self.game.current_display = self.game.main_menu


class CannonSelect(Menu):
    def __init__(self, game, number_of_player):
        super().__init__(game)
        self.players = [Player(i) for i in range(number_of_player)]
        self.cannon_selector = []

        if number_of_player <= 4:
            self.next = Button(game.screen, 760, 750, 400, 100, 5, 40, "다음")
            self.back = Button(game.screen, 760, 870, 400, 100, 5, 40, "뒤로")
        else:
            self.next = Button(game.screen, 760, 800, 400, 100, 5, 40, "다음")
            self.back = Button(game.screen, 760, 920, 400, 100, 5, 40, "뒤로")

        if number_of_player == 2:
            self.cannon_selector.append(CannonSelector(self.game.screen, 450, 200, 1.0, self.players[0]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 1090, 200, 1.0, self.players[1]))
        elif number_of_player == 3:
            self.cannon_selector.append(CannonSelector(self.game.screen, 250, 200, 1.0, self.players[0]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 770, 200, 1.0, self.players[1]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 1290, 200, 1.0, self.players[2]))
        elif number_of_player == 4:
            self.cannon_selector.append(CannonSelector(self.game.screen, 150, 200, 0.95, self.players[0]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 570, 200, 0.95, self.players[1]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 990, 200, 0.95, self.players[2]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 1410, 200, 0.95, self.players[3]))
        elif number_of_player == 5:
            self.cannon_selector.append(CannonSelector(self.game.screen, 420, 60, 0.75, self.players[0]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 820, 60, 0.75, self.players[1]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 1220, 60, 0.75, self.players[2]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 420, 430, 0.75, self.players[3]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 820, 430, 0.75, self.players[4]))
        elif number_of_player == 6:
            self.cannon_selector.append(CannonSelector(self.game.screen, 415, 60, 0.75, self.players[0]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 815, 60, 0.75, self.players[1]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 1215, 60, 0.75, self.players[2]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 415, 430, 0.75, self.players[3]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 815, 430, 0.75, self.players[4]))
            self.cannon_selector.append(CannonSelector(self.game.screen, 1215, 430, 0.75, self.players[5]))

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill("#e0e0e0")
        self.next.draw()
        self.back.draw()
        for ui in self.cannon_selector:
            ui.draw()
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

        for ui in self.cannon_selector:
            ui.event_check()

        if self.next.is_clicked():  # 다음으로
            self.game.current_display = self.game.stage_select

        if self.back.is_clicked():  # 뒤로 가기
            self.game.current_display = self.game.number_of_player_select


class StageSelect(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.stage_select = TextBox(game.screen, 660, 100, 600, 100, 70, "스테이지 선택")
        self.stage_1 = StageButton(game.screen, 450, 300, 440, 200, 5, Levels.Level1)
        self.stage_2 = StageButton(game.screen, 1030, 300, 440, 200, 5, Levels.Level2)
        self.stage_3 = StageButton(game.screen, 450, 560, 440, 200, 5, Levels.Level3)
        self.stage_4 = StageButton(game.screen, 1030, 560, 440, 200, 5, Levels.Level4)
        self.back = Button(game.screen, 760, 870, 400, 100, 5, 40, "뒤로")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill("#e0e0e0")
        self.stage_select.draw()
        self.stage_1.draw()
        self.stage_2.draw()
        self.stage_3.draw()
        self.stage_4.draw()
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
                    self.game.current_display = self.game.cannon_select

        if self.stage_1.is_clicked():  # 스테이지 1
            self.game.missile_game = MissileGame(self.game, self.game.cannon_select.players, Levels.Level1)
            pygame.mixer_music.fadeout(100)
            pygame.mixer_music.load(Resources.Sounds.Music.stage_1)
            pygame.mixer_music.play(-1)
            self.game.current_display = self.game.missile_game

        if self.stage_2.is_clicked():  # 스테이지 2
            self.game.missile_game = MissileGame(self.game, self.game.cannon_select.players, Levels.Level2)
            pygame.mixer_music.fadeout(100)
            pygame.mixer_music.load(Resources.Sounds.Music.stage_2)
            pygame.mixer_music.play(-1)
            self.game.current_display = self.game.missile_game

        if self.stage_3.is_clicked():  # 스테이지 3
            self.game.missile_game = MissileGame(self.game, self.game.cannon_select.players, Levels.Level3)
            pygame.mixer_music.fadeout(100)
            pygame.mixer_music.load(Resources.Sounds.Music.stage_3)
            pygame.mixer_music.play(-1)
            self.game.current_display = self.game.missile_game

        if self.stage_4.is_clicked():  # 스테이지 4
            self.game.missile_game = MissileGame(self.game, self.game.cannon_select.players, Levels.Level4)
            pygame.mixer_music.fadeout(100)
            pygame.mixer_music.load(Resources.Sounds.Music.stage_4)
            pygame.mixer_music.play(-1)
            self.game.current_display = self.game.missile_game

        if self.back.is_clicked():  # 대포 선택으로 돌아가기
            self.game.current_display = self.game.cannon_select


class GameMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.pause_surf = None
        self.resume = Button(game.screen, 760, 460, 400, 100, 5, 40, "계속하기")
        self.game_options = Button(game.screen, 760, 580, 400, 100, 5, 40, "설정")
        self.back_to_main_menu = Button(game.screen, 760, 700, 400, 100, 5, 40, "메인 메뉴로 돌아가기")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        if self.pause_surf is not None:
            self.game.screen.blit(self.pause_surf, (0, 0))
        else:
            self.game.screen.fill("#e0e0e0")
        self.resume.draw()
        self.game_options.draw()
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
                    pygame.mixer.unpause()
                    self.game.current_display = self.game.missile_game

        if self.resume.is_clicked():  # 게임으로
            pygame.mixer.unpause()
            self.game.current_display = self.game.missile_game

        if self.game_options.is_clicked():  # 옵션
            self.game.current_display = self.game.game_option

        if self.back_to_main_menu.is_clicked():  # 메인 메뉴로 이동
            pygame.mixer_music.load(Resources.Sounds.Music.lobby)
            pygame.mixer_music.play(-1)
            self.game.current_display = self.game.main_menu


class GameOption(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.volume = option["audio"]["volume"]
        self.keyboard_camera = option["util"]["keyboard_camera"]
        self.mouse_camera = option["util"]["mouse_camera"]
        self.title = TextBox(game.screen, 760, 100, 400, 100, 65, text='설정')

        self.volume_setting = TextBox(game.screen, 660, 250, 200, 100, 50, text='볼륨')
        self.keyboard_camera_setting = TextBox(game.screen, 410, 400, 500, 100, 50, text='키보드로 카메라 이동')
        self.mouse_camera_setting = TextBox(game.screen, 410, 550, 500, 100, 50, text='마우스로 카메라 이동')

        self.volume_display = TextBox(game.screen, 1050, 250, 100, 100, 40, text=str(self.volume), border_ratio=2)
        self.volume_up = Button(game.screen, 1170, 260, 80, 80, 4, 35, ">", border_ratio=2)
        self.volume_down = Button(game.screen, 950, 260, 80, 80, 4, 35, "<", border_ratio=2)
        self.volume_up_off = TextBox(game.screen, 1170, 258, 80, 80, 35, ">", background_color="#354b5e",
                                     border_ratio=2)
        self.volume_down_off = TextBox(game.screen, 950, 258, 80, 80, 35, "<", background_color="#354b5e",
                                       border_ratio=2)

        if self.keyboard_camera:
            self.keyboard_camera_check = Button(game.screen, 1050, 400, 100, 100, 4, 35, "O",
                                                top_color="#66a158", bottom_color="#528246", change_color="#3d5e35",
                                                border_ratio=2)
        else:
            self.keyboard_camera_check = Button(game.screen, 1050, 400, 100, 100, 4, 35, "X",
                                                top_color="#a15858", bottom_color="#824646", change_color="#5e3535",
                                                border_ratio=2)
        if self.mouse_camera:
            self.mouse_camera_check = Button(game.screen, 1050, 550, 100, 100, 4, 35, "O",
                                             top_color="#66a158", bottom_color="#528246", change_color="#3d5e35",
                                             border_ratio=2)
        else:
            self.mouse_camera_check = Button(game.screen, 1050, 550, 100, 100, 4, 35, "X",
                                             top_color="#a15858", bottom_color="#824646", change_color="#5e3535",
                                             border_ratio=2)

        self.apply = Button(game.screen, 760, 750, 400, 100, 5, 40, "적용")
        self.back = Button(game.screen, 760, 870, 400, 100, 5, 40, "뒤로")

    def loop(self):
        # 이벤트 핸들러
        self.event_check()
        # 화면 그리기
        self.game.screen.fill("#e0e0e0")
        self.title.draw()
        self.volume_setting.draw()
        self.keyboard_camera_setting.draw()
        self.mouse_camera_setting.draw()
        if self.volume < 10:
            self.volume_up.draw()
        else:
            self.volume_up_off.draw()
        if self.volume > 0:
            self.volume_down.draw()
        else:
            self.volume_down_off.draw()
        self.volume_display.draw()
        self.keyboard_camera_check.draw()
        self.mouse_camera_check.draw()
        self.apply.draw()
        self.back.draw()
        # 화면 업데이트
        if self.game.current_display == self.game.game_menu:
            self.game.screen.fill("#e0e0e0")
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_display = self.game.game_menu

        if self.volume_up.is_clicked():  # 볼륨 증가
            self.volume += 1
            self.volume_display.text_update(str(self.volume))

        if self.volume_down.is_clicked():  # 볼륨 감소
            self.volume -= 1
            self.volume_display.text_update(str(self.volume))

        if self.keyboard_camera_check.is_clicked():  # 키보드로 카메라 이동
            if self.keyboard_camera:
                self.keyboard_camera = False
                self.keyboard_camera_check.text_update("X")
                self.keyboard_camera_check.top_original_color = "#a15858"
                self.keyboard_camera_check.bottom_color = "#824646"
                self.keyboard_camera_check.change_color = "#5e3535"
            else:
                self.keyboard_camera = True
                self.keyboard_camera_check.text_update("O")
                self.keyboard_camera_check.top_original_color = "#66a158"
                self.keyboard_camera_check.bottom_color = "#528246"
                self.keyboard_camera_check.change_color = "#3d5e35"

        if self.mouse_camera_check.is_clicked():  # 키보드로 카메라 이동
            if self.mouse_camera:
                self.mouse_camera = False
                self.mouse_camera_check.text_update("X")
                self.mouse_camera_check.top_original_color = "#a15858"
                self.mouse_camera_check.bottom_color = "#824646"
                self.mouse_camera_check.change_color = "#5e3535"
            else:
                self.mouse_camera = True
                self.mouse_camera_check.text_update("O")
                self.mouse_camera_check.top_original_color = "#66a158"
                self.mouse_camera_check.bottom_color = "#528246"
                self.mouse_camera_check.change_color = "#3d5e35"

        if self.apply.is_clicked():  # 적용
            option["audio"]["volume"] = self.volume
            option["util"]["keyboard_camera"] = self.keyboard_camera
            option["util"]["mouse_camera"] = self.mouse_camera
            all_sounds.set_volume(option["audio"]["volume"] / 10)
            with open(option_file, 'w') as option_data:
                json_data = json.dumps(option, indent="\t")
                option_data.write(json_data)

        if self.back.is_clicked():  # 뒤로 가기
            self.volume = option["audio"]["volume"]
            self.volume_display.text_update(str(self.volume))
            self.game.current_display = self.game.game_menu
