from ui_component.button import *
from ui_component.textbox import *
from ui_component.bar import *
from ui_component.angle_monitor import *
from ui_component.wind_bar import *
from ui_component.power_bar import *
from config import *
import pygame


class CannonUI:
    def __init__(self, cannon):
        self.cannon = cannon
        self.screen = pygame.display.get_surface()
        self.canvas = pygame.surface.Surface((120, 200)).convert_alpha()
        self.canvas.fill((0, 0, 0, 0))
        self.canvas_rect = self.canvas.get_rect()

        self.player_name = TextBox(self.canvas, 0, 0, 120, 30, 20, self.cannon.player.name,
                                   background_color="#666666", border_ratio=2)
        self.health_bar = Bar(10, 130, 100, 20, 2, self.cannon.max_health, bar_color="#f25246", border_radius=2)

    def update(self):
        self.health_bar.level = self.cannon.health

    def draw(self):
        pygame.draw.rect(self.canvas, (255, 255, 255, 0), self.canvas_rect, border_radius=20)
        self.health_bar.draw(self.canvas)
        self.player_name.draw()
        self.screen.blit(self.canvas, self.cannon.rect.center - self.cannon.camera.offset - self.canvas_rect.center)
