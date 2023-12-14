from ui_component.button import *
from ui_component.textbox import *
from cannon import *
import os


def load_png(name, size):
    """ Load image and return image object"""
    fullname = os.path.join("Assets/Images", name)
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
        player_name_table = ["한놈", "두식이", "석삼", "너구리", "오징어", "육개장"]
        self.player.name = player_name_table[player.number]
        self.player.cannon = CANNONS[self.cannon_id]

        self.cannon_image = pygame.surface.Surface((360 * size, 360 * size)).convert_alpha()
        self.cannon_image.fill((0, 0, 0, 0))
        if self.cannon_id == 5:
            self.cannon_image.blit(load_png(CANNONS[self.cannon_id].barrel_texture, (360 * self.size, 360 * self.size)), (40, 0))
        else:
            self.cannon_image.blit(load_png(CANNONS[self.cannon_id].barrel_texture, (360 * self.size, 360 * self.size)), (0, 0))
        if CANNONS[self.cannon_id].body_texture is not None:
            self.cannon_image.blit(load_png(CANNONS[self.cannon_id].body_texture, (360 * self.size, 360 * self.size)), (0, 0))
        self.cannon_image.blit(load_png(CANNONS[self.cannon_id].wheel_texture, (360 * self.size, 360 * self.size)), (0, 0))

        self.player_name = TextBox(surface, x, y, 380 * size, 80 * size, (55 * size), self.player.name)
        self.cannon_name = TextBox(surface, x + 90 * size, y + 360 * size, 200 * size, 80 * size, (40 * size), CANNONS[self.cannon_id].name, border_ratio=2)
        self.next = Button(surface, x + 310 * size, y + 367 * size, 70 * size, 70 * size, 4 * size, (40 * size), ">", border_ratio=2)
        self.prev = Button(surface, x, y + 367 * size, 70 * size, 70 * size, 4 * size, (40 * size), "<", border_ratio=2)

    def update(self):
        self.player.cannon = CANNONS[self.cannon_id]
        self.cannon_image.fill((0, 0, 0, 0))
        if self.cannon_id == 5:
            self.cannon_image.blit(load_png(CANNONS[self.cannon_id].barrel_texture, (360 * self.size, 360 * self.size)), (40, 0))
        else:
            self.cannon_image.blit(load_png(CANNONS[self.cannon_id].barrel_texture, (360 * self.size, 360 * self.size)), (0, 0))
        if CANNONS[self.cannon_id].body_texture is not None:
            self.cannon_image.blit(load_png(CANNONS[self.cannon_id].body_texture, (360 * self.size, 360 * self.size)), (0, 0))
        self.cannon_image.blit(load_png(CANNONS[self.cannon_id].wheel_texture, (360 * self.size, 360 * self.size)), (0, 0))
        self.cannon_name.text_update(CANNONS[self.cannon_id].name)

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
            else:
                self.cannon_id = 1
            self.update()

        if self.prev.is_clicked():
            if self.cannon_id > 1:
                self.cannon_id -= 1
            else:
                self.cannon_id = len(CANNONS)
            self.update()
