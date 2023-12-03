import pygame


class Bar:
    def __init__(self, x, y, width, height, max_level):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = max_level
        self.max_level = max_level

    def draw(self, surface):
        ratio = self.level / self.max_level
        pygame.draw.rect(surface, "white", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.width * ratio, self.height))
