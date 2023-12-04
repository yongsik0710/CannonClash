from config import *
import pygame
import os


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (20, 20))
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()


class Shell(pygame.sprite.Sprite):
    texture = TexturePath.Shells.basic
    damage = 500
    explosion_radius = 50

    def __init__(self, group, stage, pos, vector, owner, cannon_group):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.depth = 2
        self.damage = self.damage
        self.radius = self.explosion_radius
        self.stage = stage
        self.cannon_group = cannon_group
        self.vector = vector
        self.owner = owner
        self.gravity = stage.gravity
        self.wind = stage.wind

        self.texture = load_png(self.texture)
        self.image, self.rect = self.texture
        self.rect = self.rect.move(pos)

        self.surf = pygame.surface.Surface((self.explosion_radius * 2, self.explosion_radius * 2)).convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.circle(self.surf, "#000000", (self.explosion_radius, self.explosion_radius), self.explosion_radius)
        self.explosion_mask = pygame.mask.from_surface(self.surf)
        # self.radius = self.explosion_radius - (self.rect.width * (2 ** (1 / 2)))
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def update(self):
        self.vector.y += self.gravity / 2
        self.vector.x += self.wind / 550
        self.collide_check()
        self.out_of_border()
        self.rect = self.rect.move(self.vector)

    def collide_check(self):
        if pygame.sprite.collide_mask(self, self.stage) or \
                pygame.sprite.spritecollide(self, self.cannon_group, False, pygame.sprite.collide_mask):
            self.explode()

    def explode(self):
        for cannon in self.cannon_group:
            pos = pygame.Vector2(self.rect.center)
            distance = pos.distance_to(cannon.rect.center)
            if distance - 25 < self.explosion_radius:
                damage = self.damage * (((self.explosion_radius - (distance - 25)) / self.explosion_radius) ** 2)
                cannon.damage(damage)
        pygame.mask.Mask.erase(self.stage.mask, self.explosion_mask, (self.rect.centerx - self.explosion_radius, self.rect.centery - self.explosion_radius))
        self.stage.custom_update()
        self.camera.target = None
        self.kill()
        self.owner.next_turn()

    def out_of_border(self):
        if self.rect.top > 2000:
            self.camera.target = None
            self.kill()
            self.owner.next_turn()


class BasicShell(Shell):
    texture = TexturePath.Shells.basic
    damage = 400
    explosion_radius = 80
