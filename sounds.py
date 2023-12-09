import pygame
from config import *


class Sounds:
    def __init__(self):
        self.sounds = []
        self.explode_sound = pygame.mixer.Sound(Resources.Sounds.explode)
        self.shoot_sound = pygame.mixer.Sound(Resources.Sounds.shoot)

        self.sounds.append(self.explode_sound)
        self.sounds.append(self.shoot_sound)

    def set_volume(self):
        for sound in self.sounds:
            sound.set_volume(Options.Audio.volume)
