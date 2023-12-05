import pygame


class Bar:
    def __init__(self, x, y, width, height, border_thickness, max_level,
                 border_color="#333333", background_color="#eeeeee", bar_color="#00ff00"):
        self.original_width = width
        self.border_color = border_color
        self.background_color = background_color
        self.bar_color = bar_color
        self.border_thickness = border_thickness
        self.level = max_level
        self.max_level = max_level

        # border rect
        self.border_rect = pygame.rect.Rect((x, y), (width, height))

        # background rect
        self.background_rect = pygame.rect.Rect((x, y), (width - (2 * border_thickness), height - (2 * border_thickness)))
        self.background_rect.center = self.border_rect.center

        # bar rect
        self.bar_rect = pygame.rect.Rect((x, y), (width - (2 * border_thickness), height - (2 * border_thickness)))
        self.bar_rect.center = self.border_rect.center

    def update(self):
        ratio = self.level / self.max_level
        self.bar_rect.width = self.original_width * ratio - (2 * self.border_thickness)

    def draw(self, surface):
        self.update()
        pygame.draw.rect(surface, self.border_color, self.border_rect, border_radius=5)
        pygame.draw.rect(surface, self.background_color, self.background_rect)
        pygame.draw.rect(surface, self.bar_color, self.bar_rect)
