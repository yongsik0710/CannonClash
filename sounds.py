import pygame


pygame.mixer.init()


class SoundGroup:
    def __init__(self):
        self.sounds = []

    def set_volume(self, volume):
        pygame.mixer_music.set_volume(volume)
        for sound in self.sounds:
            sound.set_volume(volume)


class Sound:
    def __init__(self, sound_group, sound):
        self.sound = pygame.mixer.Sound(sound)
        sound_group.sounds.append(self.sound)


all_sounds = SoundGroup()
