from bar import *
from button import *
from textbox import *
from angle_monitor import *
from config import *
import pygame


class Player:
    def __init__(self, number):
        self.number = number
        self.name = "player name"
        self.cannon = None
        self.missile_game = None
        self.player_ui = None
        self.turn = False
        self.is_death = False
        self.max_power = 180
        self.power = 0

    def death(self):
        self.turn = False
        self.is_death = True
        self.next_turn()

    def init_player_ui(self):
        self.player_ui = self.PlayerUI(self)

    def shoot_shell(self):
        if self.power <= self.max_power:
            self.cannon.shoot_shell(self.power, self)
        else:
            self.cannon.shoot_shell(self.max_power, self)
        self.power = 0
        self.turn = False

    def next_turn(self):
        self.missile_game.next_turn()

    def skip(self):
        self.missile_game.next_turn()

    def draw_player_ui(self):
        self.player_ui.update()
        self.player_ui.draw()

    class PlayerUI:
        def __init__(self, player):
            self.player = player
            self.screen = pygame.display.get_surface()
            self.canvas = pygame.surface.Surface((1400, 290)).convert_alpha()
            self.canvas.fill((255, 255, 255, 150))

            self.current_player = pygame.image.load(TexturePath.Util.current_player)

            self.player_name = TextBox(self.canvas, 40, 10, 200, 50, pygame.font.Font(None, 50), "#555555", self.player.name, False)

            self.health_bar = Bar(450, 85, 900, 40, self.player.cannon.max_health)
            self.power_bar = Bar(450, 145, 900, 40, self.player.max_power)
            self.move_bar = Bar(450, 205, 900, 40, 100)

            self.health = TextBox(self.canvas, 270, 80, 170, 50, pygame.font.Font(None, 45), "#444444", "HEALTH", False)
            self.power = TextBox(self.canvas, 270, 140, 170, 50, pygame.font.Font(None, 45), "#444444", "POWER", False)
            self.move = TextBox(self.canvas, 270, 200, 170, 50, pygame.font.Font(None, 45), "#444444", "MOVE", False)

            self.angle_monitor = AngleMonitor(self.canvas, 40, 70, self.player.cannon)
            self.wind_bar = WindBar(50, 260, 180, 20, 100)
            self.skip = Button(self.screen, 1530, 790, 100, 45, 4, pygame.font.Font(None, 35), "Skip >")

        def update(self):
            self.health_bar.level = self.player.cannon.health
            self.power_bar.level = self.player.power
            self.wind_bar.level = self.player.missile_game.stage.wind
            if self.skip.is_clicked():
                self.player.skip()

        def draw(self):
            self.screen.blit(self.current_player, self.player.cannon.rect.midtop - self.player.missile_game.camera_group.offset)

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
