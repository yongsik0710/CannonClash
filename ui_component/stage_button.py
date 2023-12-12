from sounds import *
from config import *
import pygame
import os


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image


class StageButton:
    def __init__(self, surface, x, y, width, height, border_thickness, level, inflation_size=1.1,
                 border_color="#333333"):
        # Core attributes
        self.surface = surface
        self.mouse_on_sound = Sound(all_sounds, Resources.Sounds.Util.Button.mouse_on)
        self.click_sound = Sound(all_sounds, Resources.Sounds.Util.Button.click)
        self.clicked = False
        self.pressed = False
        self.hover = False

        self.original_level_image = load_png(level.level_image)
        self.original_bg_image = load_png(level.background_image)
        self.original_image = self.original_bg_image.copy()

        self.original_image.blit(self.original_level_image, self.original_image.get_rect())

        self.border_color = border_color

        # border rectangle
        self.border_rect = pygame.rect.Rect((x, y, width, height))

        # interact rectangle
        self.interact_rect = self.border_rect.copy()

        # image surface & rect
        self.image_surf = pygame.transform.scale(self.original_image,
                                                 (width - (2 * border_thickness),
                                                  height - (2 * border_thickness)))
        self.image_rect = self.image_surf.get_rect(center=self.border_rect.center)

        # inflate border
        self.inflate_border_rect = self.border_rect.scale_by(inflation_size, inflation_size)

        # inflation image & rect
        self.inflate_image_surf = pygame.transform.scale(self.original_image,
                                                         (width * inflation_size - (2 * border_thickness),
                                                          height * inflation_size - (2 * border_thickness)))
        self.inflate_image_rect = self.inflate_image_surf.get_rect(center=self.inflate_border_rect.center)

    def draw(self):
        if self.hover:
            pygame.draw.rect(self.surface, self.border_color, self.inflate_border_rect, border_radius=6)
            self.surface.blit(self.inflate_image_surf, self.inflate_image_rect)
        else:
            pygame.draw.rect(self.surface, self.border_color, self.border_rect, border_radius=6)
            self.surface.blit(self.image_surf, self.image_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.interact_rect.collidepoint(mouse_pos):
            if not self.hover:
                self.mouse_on_sound.sound.play()
                self.hover = True
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.clicked = True
                    self.pressed = False
        else:
            self.pressed = False
            self.hover = False

    def is_clicked(self):
        if self.clicked:
            self.click_sound.sound.play()
            self.clicked = False
            return True
        return False
