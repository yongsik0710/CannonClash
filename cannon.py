from shell import *
import pygame
import os
import math


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (200, 200))
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image


class Cannon(pygame.sprite.Sprite):
    name = None
    barrel_texture = None
    wheel_texture = None
    shell = None
    default_angle = 10
    max_delta_angle = 20
    max_health = 1000
    max_mobility = 1000

    def __init__(self, group, stage, pos, vector, player):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group[0]
        self.cannon_group = group[1]
        self.player = player
        self.depth = 3

        self.health = self.max_health
        self.mobility = self.max_mobility

        self.incline_angle = 0.0
        self.delta_angle = 0.0
        self.launch_angle = 0.0

        self.on_ground = False
        self.is_death = False
        self.direction = "right"
        self.is_on_fire = False

        self.stage = stage
        self.vector = pygame.math.Vector2(vector)
        self.gravity = stage.gravity

        self.barrel = self.Barrel(self.barrel_texture)
        self.wheel = self.Wheel(self.wheel_texture)

        self.image = self.blit_cannon()
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft

        self.mask = self.wheel.mask

        self.collide_pos = (0, 0)
        self.screen = pygame.display.get_surface()

    def update(self):
        if not self.on_ground:
            self.vector.y += self.gravity / 5
        self.collide_check()
        self.angle_update()
        self.image = self.blit_cannon()
        self.rect = self.rect.move(self.vector)
        self.vector.x = 0
        self.out_of_border()

    def blit_cannon(self):
        surf = pygame.surface.Surface((200, 200)).convert_alpha()
        surf.fill((0, 0, 0, 0))

        if self.direction == "right":
            self.barrel.blit(surf, (0, 0), self.launch_angle)
            if self.is_on_fire:
                fire = load_png(TexturePath.Shells.fireball)
                fire = pygame.transform.rotozoom(fire, -90, 0.5)
                surf.blit(fire, (50, 50))
            self.wheel.blit(surf, (0, 0))
        elif self.direction == "left":
            self.barrel.blit(surf, (0, 0), self.launch_angle)
            if self.is_on_fire:
                fire = load_png(TexturePath.Shells.fireball)
                fire = pygame.transform.rotozoom(fire, -90, 0.5)
                surf.blit(fire, (50, 50))
            surf = pygame.transform.flip(surf, True, False)
            self.wheel.blit(surf, (0, 0))

        return surf

    def angle_update(self):
        surf = pygame.surface.Surface((48, 48)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        surf.blit(self.stage.image, (-(self.rect.centerx - 24), -self.rect.centery))
        mask = pygame.mask.from_surface(surf)

        border_bits = []
        for x in range(48):
            for y in range(48):
                if mask.get_at((x, y)):
                    border_bits.append((x, y))
                    break

        sum_of_angles = [0, 0]
        for i in range(len(border_bits)):
            sum_of_angles[0] += border_bits[i][0] - border_bits[0][0]
            sum_of_angles[1] += border_bits[i][1] - border_bits[0][1]

        self.incline_angle = pygame.Vector2(sum_of_angles[0], sum_of_angles[1]).angle_to((0, 0))

        if self.direction == "right":
            self.launch_angle = self.default_angle + self.incline_angle + self.delta_angle
        else:
            self.launch_angle = self.default_angle - self.incline_angle + self.delta_angle

    def collide_check(self):
        if pygame.sprite.collide_mask(self, self.stage):
            self.on_ground = True
            if self.mask.overlap(self.stage.mask, (-self.rect.x, -self.rect.y + 3)):
                self.vector.y = -2
            else:
                self.collide_pos = self.mask.overlap(self.stage.mask, (-self.rect.centerx, -self.rect.centery))
                # self.collide_pos = (self.collide_pos[0] + self.rect.x, self.collide_pos[1] + self.rect.y)
                self.vector.y = 0
        else:
            self.on_ground = False

    def shoot_shell(self, power, owner):
        if self.direction == "right":
            vector = pygame.Vector2([math.cos(math.radians(self.launch_angle)), - math.sin(math.radians(self.launch_angle))])
            rotated_launch_vector = vector.copy().rotate(90)

        else:
            vector = pygame.Vector2([- math.cos(math.radians(self.launch_angle)), - math.sin(math.radians(self.launch_angle))])
            rotated_launch_vector = vector.copy().rotate(-90)

        vector.scale_to_length(power / 3)
        scaled_launch_vector = vector.copy()
        scaled_launch_vector.scale_to_length(80)
        rotated_launch_vector.scale_to_length(30)
        rotated_launch_vector -= scaled_launch_vector
        self.camera.target = self.shell(self.camera, self.stage, self.rect.center - rotated_launch_vector, vector, owner, self.cannon_group)

    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_death = True
            self.player.death()

    def out_of_border(self):
        if self.rect.top > 2000:
            self.is_death = True
            self.player.death()
            self.kill()

    def angle_up(self):
        if self.delta_angle + 1 <= self.max_delta_angle:
            self.delta_angle += 1
        else:
            self.delta_angle = self.max_delta_angle

    def angle_down(self):
        if self.delta_angle - 1 >= -self.max_delta_angle:
            self.delta_angle -= 1
        else:
            self.delta_angle = -self.max_delta_angle

    def move_right(self):
        self.direction = "right"
        if self.mobility > 0 and self.incline_angle <= 55:
            self.vector.x = 1
            self.wheel.roll_cw()
            if self.incline_angle >= 0:
                delta_mobility = (6 + abs(self.incline_angle) / 4)
            else:
                delta_mobility = 6
            if self.mobility - delta_mobility >= 0:
                self.mobility -= delta_mobility
            else:
                self.mobility = 0

    def move_left(self):
        self.direction = "left"
        if self.mobility > 0 and self.incline_angle >= -55:
            self.vector.x = -1
            self.wheel.roll_acw()
            if self.incline_angle <= 0:
                delta_mobility = (6 + abs(self.incline_angle) / 4)
            else:
                delta_mobility = 6
            if self.mobility - delta_mobility >= 0:
                self.mobility -= delta_mobility
            else:
                self.mobility = 0

    class Barrel:
        def __init__(self, texture):
            self.image = load_png(texture)
            self.rect = self.image.get_rect()

        def blit(self, surf, topleft, angle):
            rotated_image = pygame.transform.rotate(self.image, angle)
            new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=topleft).center)

            surf.blit(rotated_image, new_rect)

    class Wheel:
        def __init__(self, texture):
            self.image = load_png(texture)
            self.mask = pygame.mask.from_surface(self.image)
            self.angle = 0.0

        def blit(self, surf, topleft):
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=topleft).center)

            surf.blit(rotated_image, new_rect)

        def roll_cw(self):
            self.angle -= 2

        def roll_acw(self):
            self.angle += 2


class BasicCannon(Cannon):
    name = "대포"
    barrel_texture = TexturePath.Cannons.Barrel.basic_barrel
    wheel_texture = TexturePath.Cannons.Wheel.basic_wheel
    shell = BasicShell
    default_angle = 20
    max_delta_angle = 20


class Ballista(Cannon):
    name = "발리스타"
    barrel_texture = TexturePath.Cannons.Barrel.ballista_barrel
    wheel_texture = TexturePath.Cannons.Wheel.ballista_wheel
    shell = Arrow
    default_angle = 40
    max_delta_angle = 10


class FlameCannon(Cannon):
    name = "화포"
    barrel_texture = TexturePath.Cannons.Barrel.flame_cannon_barrel
    wheel_texture = TexturePath.Cannons.Wheel.flame_cannon_wheel
    shell = FireBall
    default_angle = 20
    max_delta_angle = 30


CANNONS = {
    1: BasicCannon,
    2: Ballista,
    3: FlameCannon
}