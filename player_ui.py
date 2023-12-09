from ui_component.button import *
from ui_component.textbox import *
from ui_component.bar import *
from ui_component.angle_monitor import *
from ui_component.wind_bar import *
from ui_component.power_bar import *
from config import *
import pygame


class PlayerUI:
    def __init__(self, player):
        self.player = player
        self.screen = pygame.display.get_surface()
        self.canvas = pygame.surface.Surface((1400, 290)).convert_alpha()
        self.canvas.fill((0, 0, 0, 0))
        self.canvas_rect = self.canvas.get_rect()

        self.current_player = pygame.image.load(Resources.Util.current_player)

        self.player_name = TextBox(self.canvas, 40, 10, 200, 50, 35, self.player.name,
                                   background_color="#555555", border_ratio=2)

        self.health_bar = Bar(450, 85, 900, 40, 5, self.player.cannon.max_health, bar_color="#f25246")
        self.power_bar = PowerBar(450, 145, 900, 40, 5, self.player.max_power, bar_color="#5fe84d")
        self.move_bar = Bar(450, 205, 900, 40, 5, self.player.cannon.max_mobility, bar_color="#ffcd45")

        self.health = TextBox(self.canvas, 270, 80, 170, 50, 30, "HEALTH",
                              background_color="#f25246", border_ratio=2)
        self.power = TextBox(self.canvas, 270, 140, 170, 50, 30, "POWER",
                             background_color="#5fe84d", border_ratio=2)
        self.move = TextBox(self.canvas, 270, 200, 170, 50, 30, "MOVE",
                            background_color="#ffcd45", border_ratio=2)

        self.angle_monitor = AngleMonitor(self.canvas, 40, 70, self.player.cannon)
        self.wind_bar = WindBar(50, 245, 180, 25, 2, 100, bar_color="#75e8ff")
        self.skip = Button(self.screen, 1530, 790, 100, 45, 4, 25, "Skip >", border_ratio=2)

    def update(self):
        self.health_bar.level = self.player.cannon.health
        self.power_bar.level = self.player.power
        self.move_bar.level = self.player.cannon.mobility
        self.wind_bar.level = self.player.missile_game.stage.wind
        if self.skip.is_clicked():
            self.player.skip()

    def draw(self):
        self.screen.blit(self.current_player, self.player.cannon.rect.midtop - self.player.missile_game.camera_group.offset)

        pygame.draw.rect(self.canvas, (255, 255, 255, 150), self.canvas_rect, border_radius=20)
        self.angle_monitor.draw()
        self.health_bar.draw(self.canvas)
        self.power_bar.draw(self.canvas)
        self.move_bar.draw(self.canvas)
        self.wind_bar.draw(self.canvas)
        self.health.draw()
        self.power.draw()
        self.move.draw()
        self.player_name.draw()
        self.screen.blit(self.canvas, (260, 770))
        self.skip.draw()
