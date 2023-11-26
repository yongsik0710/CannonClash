import pygame


class TextBox:
    def __init__(self, surface, x, y, width, height, font, background_color, text="button", transparent=False):
        # Core attributes
        self.surface = surface
        self.text = text
        self.font = font
        self.transparent = transparent

        # background rectangle
        self.background_rect = pygame.Rect((x, y), (width, height))
        self.background_color = background_color

        # text
        self.text_surf = self.font.render(self.text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.background_rect.center)

    def draw(self):
        self.update()
        if not self.transparent:
            pygame.draw.rect(self.surface, self.background_color, self.background_rect, border_radius=12)
        self.surface.blit(self.text_surf, self.text_rect)

    def update(self):
        # text update
        self.text_surf = self.font.render(self.text, True, '#FFFFFF')
