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


class WindBar(Bar):
    def draw(self, surface):
        ratio = self.level / self.max_level
        pygame.draw.rect(surface, "white", (self.x, self.y, self.width, self.height))
        if ratio >= 0:
            pygame.draw.rect(surface, "green", (self.x + (self.width / 2), self.y, self.width * ratio / 2, self.height))
        else:
            pygame.draw.rect(surface, "green", (self.x + (self.width - self.width * (-ratio)) / 2, self.y, self.width * (-ratio) / 2, self.height))

        pygame.draw.line(surface, "#000000", (self.x + (self.width / 2) - 1, self.y), (self.x + (self.width / 2) - 1, self.y + self.height), 3)
