from ui_component.bar import *


class PowerBar(Bar):
    def __init__(self, x, y, width, height, border_thickness, max_level,
                 border_color="#333333", background_color="#eeeeee", bar_color="#00ff00"):
        Bar.__init__(self, x, y, width, height, border_thickness, max_level,
                     border_color, background_color, bar_color)

        self.prev_power = 1
        self.line_x = 0

    def draw(self, surface):
        self.update()
        pygame.draw.rect(surface, self.border_color, self.border_rect, border_radius=5)
        pygame.draw.rect(surface, self.background_color, self.background_rect)
        pygame.draw.rect(surface, self.bar_color, self.bar_rect)
        ratio = self.prev_power / self.max_level
        self.line_x = self.bar_rect.x + self.original_width * ratio - (2 * self.border_thickness)
        pygame.draw.line(surface, self.border_color, (self.line_x, self.bar_rect.top), (self.line_x, self.bar_rect.bottom), 2)
