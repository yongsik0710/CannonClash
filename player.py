from bar import *
from button import *
import pygame


class Player:
    def __init__(self, number):
        self.number = number
        self.name = "player name"
        self.cannon = None
        self.missile_game = None
        self.player_ui = None
        self.turn = False
        self.max_power = 180
        self.power = 0

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

    def draw_player_ui(self):
        self.player_ui.update()
        self.player_ui.draw()

    class PlayerUI:
        def __init__(self, player):
            self.player = player
            self.health_bar = Bar(400, 50, 1000, 30, self.player.cannon.max_health)
            self.power_bar = Bar(400, 100, 1000, 30, self.player.max_power)
            self.screen = pygame.display.get_surface()
            self.skip = Button(self.screen, 1600, 800, 100, 50, 4, pygame.font.Font(None, 40), "Skip")

        def update(self):
            self.health_bar.level = self.player.cannon.health
            self.power_bar.level = self.player.power
            if self.skip.is_clicked():
                self.player.next_turn()

        def draw(self):
            surf = pygame.surface.Surface((1600, 250)).convert_alpha()
            surf.fill((255, 255, 255, 120))
            self.health_bar.draw(surf)
            self.power_bar.draw(surf)
            self.screen.blit(surf, (160, 780))
            self.skip.draw()
