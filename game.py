import pygame
from menu import *


class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1920, 1080
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("대포 게임")
        self.clock = pygame.time.Clock()
        self.FPS = 60

    def start_game(self):
        MainMenu(self)
