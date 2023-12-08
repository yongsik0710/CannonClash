from config import *
from spritesheet import *
import pygame
import os


def load_png(name, size):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale_by(image, size)
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
    texture_size = 1
    damage = 100
    explosion_radius = 50

    def __init__(self, group, stage, pos, vector, owner, cannon_group):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.depth = 2
        self.damage = self.damage
        self.stage = stage
        self.cannon_group = cannon_group
        self.vector = vector
        self.owner = owner
        self.gravity = stage.gravity
        self.wind = stage.wind

        self.image, self.rect = load_png(self.texture, self.texture_size)
        self.rect.center = self.rect.move(pos).topleft
        self.original_image = self.image.copy()

        ellipse_rect = pygame.rect.Rect((0, 0), (self.explosion_radius * 3, self.explosion_radius * 2))
        self.surf = pygame.surface.Surface(ellipse_rect.size).convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.surf, "#000000", ellipse_rect)
        self.explosion_mask = pygame.mask.from_surface(self.surf)

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
            if 0 <= distance - 30 <= self.explosion_radius:
                damage = self.damage * (((self.explosion_radius - (distance - 30)) / self.explosion_radius) ** 2)
                cannon.damage(damage)
            elif distance < 30:
                damage = self.damage
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
    texture_size = 0.7
    damage = 300
    explosion_radius = 60


class Arrow(Shell):
    texture = TexturePath.Shells.arrow
    texture_size = 1
    damage = 100
    explosion_radius = 30

    def update(self):
        self.vector.y += self.gravity / 2
        self.vector.x += self.wind / 550
        angle = self.vector.angle_to((0, 0))
        self.image, self.rect = self.rot_center(angle, self.rect.centerx, self.rect.centery)
        self.collide_check()
        self.out_of_border()
        self.rect = self.rect.move(self.vector)

    def rot_center(self, angle, x, y):
        rotated_image = pygame.transform.rotate(self.original_image, angle)
        new_rect = rotated_image.get_rect(center=self.original_image.get_rect(center=(x, y)).center)

        return rotated_image, new_rect

    def explode(self):
        for cannon in self.cannon_group:
            pos = pygame.Vector2(self.rect.center)
            distance = pos.distance_to(cannon.rect.center)
            if 0 <= distance - 50 <= self.explosion_radius:
                damage = self.damage * (self.vector.length_squared() / 500)
                damage *= ((self.explosion_radius - (distance - 50)) / self.explosion_radius) ** 2
                cannon.damage(damage)
            elif distance < 50:
                damage = self.damage * (self.vector.length_squared() / 500)
                cannon.damage(damage)
        pygame.mask.Mask.erase(self.stage.mask, self.explosion_mask, (self.rect.centerx - self.explosion_radius, self.rect.centery - self.explosion_radius))
        self.stage.custom_update()
        self.camera.target = None
        self.kill()
        self.owner.next_turn()


class FireBall(Shell):
    texture = TexturePath.Shells.fireball
    texture_size = 0.55
    damage = 250
    explosion_radius = 60

    def __init__(self, group, stage, pos, vector, owner, cannon_group):
        Shell.__init__(self, group, stage, pos, vector, owner, cannon_group)
        self.sprites = SpriteSheet(self.texture, 5, self.texture_size).sprites
        self.current_frame = 0
        self.anim_speed = 0.25

        self.image = self.sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft
        self.original_image = self.image.copy()

    def update(self):
        self.vector.y += self.gravity / 2
        self.vector.x += self.wind / 550

        self.image = self.sprites[int(self.current_frame)]
        self.original_image = self.image.copy()
        self.current_frame += self.anim_speed
        if int(self.current_frame) >= len(self.sprites):
            self.current_frame = 0
        angle = self.vector.angle_to((0, 0))
        self.image, self.rect = self.rot_center(angle, self.rect.centerx, self.rect.centery)
        self.collide_check()
        self.out_of_border()
        self.rect = self.rect.move(self.vector)

    def rot_center(self, angle, x, y):
        rotated_image = pygame.transform.rotate(self.original_image, angle)
        new_rect = rotated_image.get_rect(center=self.original_image.get_rect(center=(x, y)).center)

        return rotated_image, new_rect

    def explode(self):
        for cannon in self.cannon_group:
            pos = pygame.Vector2(self.rect.center)
            distance = pos.distance_to(cannon.rect.center)
            if 0 <= distance - 30 <= self.explosion_radius:
                damage = self.damage * (((self.explosion_radius - (distance - 30)) / self.explosion_radius) ** 2)
                cannon.damage(damage)
                cannon.is_on_fire = True
            elif distance < 30:
                damage = self.damage
                cannon.damage(damage)
                cannon.is_on_fire = True

        pygame.mask.Mask.erase(self.stage.mask, self.explosion_mask, (self.rect.centerx - self.explosion_radius, self.rect.centery - self.explosion_radius))
        self.stage.custom_update()
        self.camera.target = None
        self.kill()
        self.owner.next_turn()
