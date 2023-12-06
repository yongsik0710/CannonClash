from config import *
import pygame


class TextBox:
    def __init__(self, surface, x, y, width, height, font_size, text="button", font_path=FontPath.font,
                 background_color="#808080", text_color="#ffffff", transparent=False):
        # Core attributes
        self.surface = surface
        self.text = text
        self.font = pygame.font.Font(font_path, int(font_size * 0.7))
        self.original_height = height
        self.background_color = background_color
        self.text_color = text_color
        self.transparent = transparent

        # background rectangle
        self.background_rect = pygame.Rect((x, y), (width, height))

        # text
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.background_rect.center)

    def draw(self):
        if not self.transparent:
            pygame.draw.rect(self.surface, self.background_color, self.background_rect, border_radius=int(self.original_height/6))
        self.surface.blit(self.text_surf, self.text_rect)

    def text_update(self, text):
        # text update
        self.text = text
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.background_rect.center)
