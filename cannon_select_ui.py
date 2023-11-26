from button import *
from textbox import *
from config import *
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


class CannonSelectUI:
    def __init__(self, surface, x, y, title_font, font, player_name):
        self.screen = surface
        self.x = x
        self.y = y
        self.surf = pygame.surface.Surface((240, 240)).convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        self.surf.blit(load_png(Texture.Cannon.Barrel.cannon_1), (0, 0))
        self.surf.blit(load_png(Texture.Cannon.Wheel.wheel_1), (0, 0))

        self.player_name = TextBox(surface, x, y, 380, 80, title_font, '#808080', player_name)
        self.cannon = TextBox(surface, x, y + 350, 380, 100, font, '#000000', "Cannon 1", True)
        self.next = Button(surface, x + 300, y + 360, 80, 80, 5, font, ">")
        self.prev = Button(surface, x, y + 360, 80, 80, 5, font, "<")

    def update(self):
        pass

    def draw(self):
        self.player_name.draw()
        self.cannon.draw()
        self.screen.blit(self.surf, (self.x + 70, self.y + 90))
        self.next.draw()
        self.prev.draw()
