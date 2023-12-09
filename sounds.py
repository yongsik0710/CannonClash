import pygame
from config import *


def set_volume(volume):
    for sound in sounds:
        sound.set_volume(volume)


explode_sound = pygame.mixer.Sound(Resources.Sounds.explode)
shoot_sound = pygame.mixer.Sound(Resources.Sounds.shoot)
