from menu import *


class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1920, 1080
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Cannon Clash")
        pygame.display.set_icon(load_png(Resources.icon))
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.missile_game = None
        self.game_menu = GameMenu(self)
        self.game_option = GameOption(self)
        self.main_menu = MainMenu(self)
        self.game_explain = GameExplain(self)
        self.option = Option(self)
        self.number_of_player_select = NumberOfPlayerSelect(self)
        self.cannon_select = None
        self.stage_select = StageSelect(self)
        self.game_end = None
        self.current_display = self.main_menu

    def start_game(self):
        pygame.mixer_music.load(Resources.Sounds.Music.lobby)
        pygame.mixer_music.play(-1)
        all_sounds.set_volume(option["audio"]["volume"] / 10)
        self.main_loop()

    def main_loop(self):
        running = True
        while running:
            self.current_display.loop()
            if self.current_display.stop:
                running = False
