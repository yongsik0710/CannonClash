from config import *
import pygame


class Button:
    def __init__(self, surface, x, y, width, height, elevation, font_size, text="button", font_path=FontPath.font, border_ratio=6,
                 top_color="#475f77", bottom_color="#354b5e", change_color="#d74b4b"):
        # Core attributes
        self.surface = surface
        font = pygame.font.Font(font_path, int(font_size))
        self.clicked = False
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = y
        self.original_height = height

        self.top_original_color = top_color
        self.bottom_color = bottom_color
        self.change_color = change_color

        self.border_ratio = border_ratio

        # interact rectangle
        self.interact_rect = pygame.Rect((x, y - self.elevation), (width, height))

        # top rectangle
        self.top_rect = pygame.Rect((x, y), (width, height))
        self.top_color = self.top_original_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect((x, y), (width, height))

        # text
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(self.surface, self.bottom_color, self.bottom_rect, border_radius=int(self.original_height / self.border_ratio))
        pygame.draw.rect(self.surface, self.top_color, self.top_rect, border_radius=int(self.original_height / self.border_ratio))
        self.surface.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.interact_rect.collidepoint(mouse_pos):
            self.top_color = self.change_color
            if pygame.mouse.get_pressed()[0]:
                self.interact_rect.height = self.original_height + self.elevation
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed:
                    self.clicked = True
                    self.interact_rect.height = self.original_height
                    self.pressed = False
        else:
            self.interact_rect.height = self.original_height
            self.pressed = False
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_original_color

    def is_clicked(self):
        if self.clicked:
            self.clicked = False
            return True
        return False
