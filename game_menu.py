import pygame
from config import *
from button import *


button_image = pygame.image.load(Texture.Buttons.button).convert_alpha()


class GameMenu:
    resume_button = Button(500, 100, button_image, 1)
    exit_button = Button(500, 200, button_image, 1)

    def process(self, surface):
        if self.resume_button.draw(surface):
            game_stage = "play"
