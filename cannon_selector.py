from button import *
from textbox import *
from cannon import *
import os


def load_png(name, size):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, size)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image


class CannonSelector:
    def __init__(self, surface, x, y, size, player):
        self.screen = surface
        self.x = x
        self.y = y
        self.size = size
        self.cannon_id = 1
        self.player = player
        self.player.name = "Player " + str(player.number + 1)
        self.player.cannon = CANNONS[self.cannon_id]

        font = pygame.font.Font(None, int(50 * size))
        title_font = pygame.font.Font(None, int(80 * size))

        self.cannon_image = pygame.surface.Surface((360 * size, 360 * size)).convert_alpha()
        self.cannon_image.fill((0, 0, 0, 0))
        self.cannon_image.blit(load_png(CANNONS[self.cannon_id].barrel_texture, (360 * self.size, 360 * self.size)), (0, 0))
        self.cannon_image.blit(load_png(CANNONS[self.cannon_id].wheel_texture, (360 * self.size, 360 * self.size)), (0, 0))

        self.player_name = TextBox(surface, x, y, 380 * size, 80 * size, title_font, '#808080', self.player.name)
        self.cannon_name = TextBox(surface, x + 90 * size, y + 360 * size, 200 * size, 80 * size, font, '#808080', CANNONS[self.cannon_id].name)
        self.next = Button(surface, x + 300 * size, y + 360 * size, 80 * size, 80 * size, 5 * size, font, ">")
        self.prev = Button(surface, x, y + 360 * size, 80 * size, 80 * size, 5 * size, font, "<")

    def update(self):
        self.player.cannon = CANNONS[self.cannon_id]
        self.cannon_image.fill((0, 0, 0, 0))
        self.cannon_image.blit(load_png(CANNONS[self.cannon_id].barrel_texture, (360 * self.size, 360 * self.size)), (0, 0))
        self.cannon_image.blit(load_png(CANNONS[self.cannon_id].wheel_texture, (360 * self.size, 360 * self.size)), (0, 0))
        self.cannon_name.text = CANNONS[self.cannon_id].name

    def draw(self):
        self.player_name.draw()
        self.cannon_name.draw()
        self.screen.blit(self.cannon_image, (self.x, self.y + 80 * self.size))
        self.next.draw()
        self.prev.draw()

    def event_check(self):
        if self.next.is_clicked():
            if self.cannon_id < len(CANNONS):
                self.cannon_id += 1
                self.update()

        if self.prev.is_clicked():
            if self.cannon_id > 1:
                self.cannon_id -= 1
                self.update()
