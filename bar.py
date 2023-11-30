import pygame


class Bar:
    def __init__(self, x, y, width, height, max):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = max
        self.max = max

    def draw(self, surface):
        ratio = self.level / self.max
        pygame.draw.rect(surface, "red", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.width * ratio, self.height))
