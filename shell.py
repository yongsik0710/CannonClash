import random

from config import *
from effect import *
from sounds import *
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
    texture = Resources.Texture.Shells.basic
    texture_size = 1
    explode_sound = Sound(all_sounds, Resources.Sounds.Shell.Basic.explode)
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
        self.angle = 0.0

        self.image, self.rect = load_png(self.texture, self.texture_size)
        self.rect.center = self.rect.move(pos).topleft
        self.original_image = self.image.copy()

        self.explosion_rect = pygame.rect.Rect((0, 0), (self.explosion_radius * 3, self.explosion_radius * 2))
        self.surf = pygame.surface.Surface(self.explosion_rect.size).convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.surf, "#000000", self.explosion_rect)
        self.explosion_mask = pygame.mask.from_surface(self.surf)

    def update(self):
        self.vector.y += self.gravity / 2
        self.vector.x += self.wind / 600

        self.angle += 10
        self.image, self.rect = self.rot_center(self.angle, self.rect.centerx, self.rect.centery)

        self.collide_check()
        self.out_of_border()
        self.rect = self.rect.move(self.vector)

    def rot_center(self, angle, x, y):
        rotated_image = pygame.transform.rotate(self.original_image, angle)
        new_rect = rotated_image.get_rect(center=self.original_image.get_rect(center=(x, y)).center)

        return rotated_image, new_rect

    def collide_check(self):
        if pygame.sprite.collide_mask(self, self.stage) or \
                pygame.sprite.spritecollide(self, self.cannon_group, False, pygame.sprite.collide_mask):
            self.explode()

    def explode(self):
        for cannon in self.cannon_group:
            pos = pygame.Vector2(self.rect.center)
            distance = pos.distance_to(cannon.rect.center)
            if 0 <= distance - 40 <= self.explosion_radius:
                damage = self.damage * (((self.explosion_radius - (distance - 40)) / self.explosion_radius) ** 2)
                cannon.damage(damage)
            elif distance < 40:
                damage = self.damage
                cannon.damage(damage)

        pygame.mask.Mask.erase(self.stage.mask, self.explosion_mask,
                               (self.rect.centerx - (self.explosion_rect.width / 2),
                                self.rect.centery - (self.explosion_rect.height / 2)))
        self.stage.custom_update()
        Explosion(self.camera, self.rect.center, Resources.Texture.Effects.explosion_1, 7, 1.3, 0.20, self.owner)
        self.camera.particle_destroy.summon_particles(self.rect.center, 0, 20)
        self.explode_sound.sound.play()
        self.kill()

    def out_of_border(self):
        if self.rect.top > 2000:
            self.camera.target = None
            self.kill()
            self.owner.next_turn()


class BasicShell(Shell):
    texture = Resources.Texture.Shells.basic
    texture_size = 0.7
    explode_sound = Sound(all_sounds, Resources.Sounds.Shell.Basic.explode)
    damage = 300
    explosion_radius = 80


class Arrow(Shell):
    texture = Resources.Texture.Shells.arrow
    texture_size = 1
    explode_sound = Sound(all_sounds, Resources.Sounds.Shell.Arrow.explode)
    damage = 100
    explosion_radius = 30

    def update(self):
        self.vector.y += self.gravity / 2
        self.vector.x += self.wind / 600

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
            if 0 <= distance - 56 <= self.explosion_radius:
                damage = (2 * self.damage) + self.damage * (self.vector.length_squared() / 600)
                damage *= ((self.explosion_radius - (distance - 56)) / self.explosion_radius) ** 2
                cannon.damage(damage)
            elif distance < 56:
                damage = (2 * self.damage) + self.damage * (self.vector.length_squared() / 600)
                cannon.damage(damage)
        pygame.mask.Mask.erase(self.stage.mask, self.explosion_mask,
                               (self.rect.centerx - (self.explosion_rect.width / 2),
                                self.rect.centery - (self.explosion_rect.height / 2)))
        self.stage.custom_update()
        self.camera.particle_destroy.summon_particles(self.rect.center, 0, 20)
        self.explode_sound.sound.play()
        self.camera.target = None
        self.owner.next_turn()
        self.kill()


class FireBall(Shell):
    texture = Resources.Texture.Shells.fireball
    texture_size = 0.5
    explode_sound = Sound(all_sounds, Resources.Sounds.Shell.Fireball.explode)
    damage = 230
    explosion_radius = 60

    def __init__(self, group, stage, pos, vector, owner, cannon_group):
        Shell.__init__(self, group, stage, pos, vector, owner, cannon_group)
        self.sprite_sheet = SpriteSheet(self.texture, 5)
        self.current_frame = 0
        self.animation_speed = 0.25

        self.image = self.sprite_sheet.get_image(int(self.current_frame), self.texture_size)
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft
        self.original_image = self.image.copy()

    def update(self):
        self.vector.y += self.gravity / 2
        self.vector.x += self.wind / 600

        self.image = self.sprite_sheet.get_image(int(self.current_frame), self.texture_size)
        self.original_image = self.image.copy()
        self.current_frame += self.animation_speed
        if int(self.current_frame) >= self.sprite_sheet.frame:
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
            if 0 <= distance - 75 <= self.explosion_radius:
                damage = self.damage * (((self.explosion_radius - (distance - 75)) / self.explosion_radius) ** 2)
                cannon.damage(damage)
                if cannon.fire_turn < 2 and damage > 10:
                    cannon.fire_turn = 2
                    if cannon.fire_effect is None:
                        cannon.fire_effect = Fire(self.camera, cannon, cannon.rect.center, Resources.Texture.Effects.fire, 5, 0.7, 0.25, loop=True)
            elif distance < 75:
                damage = self.damage
                cannon.damage(damage)
                cannon.fire_turn = random.randint(2, 4)
                if cannon.fire_effect is None:
                    cannon.fire_effect = Fire(self.camera, cannon, cannon.rect.center, Resources.Texture.Effects.fire, 5, 0.7, 0.25, loop=True)

        pygame.mask.Mask.erase(self.stage.mask, self.explosion_mask,
                               (self.rect.centerx - (self.explosion_rect.width / 2),
                                self.rect.centery - (self.explosion_rect.height / 2)))
        self.stage.custom_update()
        Explosion(self.camera, self.rect.center, Resources.Texture.Effects.explosion_1, 7, 1.1, 0.2, self.owner)
        self.camera.particle_flame.summon_particles(self.rect.center, 10, 20)
        self.explode_sound.sound.play()
        self.kill()


class Stone(Shell):
    texture = Resources.Texture.Shells.stone
    texture_size = 1
    explode_sound = Sound(all_sounds, Resources.Sounds.Shell.Stone.explode)
    damage = 400
    explosion_radius = 60

    def explode(self):
        for cannon in self.cannon_group:
            pos = pygame.Vector2(self.rect.center)
            distance = pos.distance_to(cannon.rect.center)
            if 0 <= distance - 70 <= self.explosion_radius:
                damage = self.damage * (((self.explosion_radius - (distance - 70)) / self.explosion_radius) ** 2)
                cannon.damage(damage)
            elif distance < 70:
                damage = self.damage
                cannon.damage(damage)

        pygame.mask.Mask.erase(self.stage.mask, self.explosion_mask,
                               (self.rect.centerx - (self.explosion_rect.width / 2),
                                self.rect.centery - (self.explosion_rect.height / 2)))
        self.stage.custom_update()
        Explosion(self.camera, self.rect.center, Resources.Texture.Effects.explosion_1, 7, 1.1, 0.2, self.owner)
        self.camera.particle_destroy.summon_particles(self.rect.center, 10, 30)
        self.explode_sound.sound.play()
        self.kill()


class Missile(Shell):
    texture = Resources.Texture.Shells.missile
    texture_size = 1.2
    explode_sound = Sound(all_sounds, Resources.Sounds.Shell.Missile.explode)
    damage = 350
    explosion_radius = 60

    def update(self):
        self.vector.y += self.gravity / 2
        self.vector.x += self.wind / 600

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
            if 0 <= distance - 51 <= self.explosion_radius:
                damage = self.damage * (((self.explosion_radius - (distance - 51)) / self.explosion_radius) ** 2)
                cannon.damage(damage)
            elif distance < 51:
                damage = self.damage
                cannon.damage(damage)

        pygame.mask.Mask.erase(self.stage.mask, self.explosion_mask,
                               (self.rect.centerx - (self.explosion_rect.width / 2),
                                self.rect.centery - (self.explosion_rect.height / 2)))
        self.stage.custom_update()
        Explosion(self.camera, self.rect.center, Resources.Texture.Effects.explosion_2, 42, 1, 1, self.owner)
        self.camera.particle_destroy.summon_particles(self.rect.center, 0, 20)
        self.explode_sound.sound.play()
        self.kill()
