import random

from shell import *
from cannon_ui import *
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
    body_texture = None
    wheel_texture = None
    shell = None
    shoot_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.shoot)
    damage_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.damage)
    barrel_move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.barrel_move)
    move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.move)
    burning_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.burning)
    barrel_length = 80
    barrel_distance = 30

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
        self.fire_turn = 0
        self.fire_effect = None

        self.stage = stage
        self.vector = pygame.math.Vector2(vector)
        self.gravity = stage.gravity

        self.barrel = self.Barrel(self.barrel_texture)
        self.wheel = self.Wheel(self.wheel_texture)
        self.cannon_ui = CannonUI(self)

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
            self.wheel.blit(surf, (0, 0))
        elif self.direction == "left":
            self.barrel.blit(surf, (0, 0), self.launch_angle)
            surf = pygame.transform.flip(surf, True, False)
            self.wheel.blit(surf, (0, 0))

        return surf

    def draw_cannon_ui(self):
        self.cannon_ui.update()
        self.cannon_ui.draw()

    def angle_update(self):
        surf = pygame.surface.Surface((32, 32)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        surf.blit(self.stage.image, (-(self.rect.centerx - 16), -self.rect.centery))
        mask = pygame.mask.from_surface(surf)

        border_bits = []
        for x in range(32):
            for y in range(32):
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
        dy = 0
        self.on_ground = True
        try:
            while not self.stage.mask.get_at((self.rect.centerx, self.rect.centery + dy)):
                dy += 1

            if 0 <= dy <= 24:
                self.rect.centery = (self.rect.centery - 24) + dy
            else:
                self.on_ground = False
        except:
            self.on_ground = False

        if self.on_ground:
            self.vector.y = 0

    def shoot_shell(self, power, owner):
        if self.direction == "right":
            vector = pygame.Vector2([math.cos(math.radians(self.launch_angle)), - math.sin(math.radians(self.launch_angle))])
            rotated_launch_vector = vector.copy().rotate(90).normalize()

        else:
            vector = pygame.Vector2([- math.cos(math.radians(self.launch_angle)), - math.sin(math.radians(self.launch_angle))])
            rotated_launch_vector = vector.copy().rotate(-90).normalize()

        vector.scale_to_length(power / 3)
        scaled_launch_vector = vector.copy().normalize()
        scaled_launch_vector.scale_to_length(self.barrel_length)
        rotated_launch_vector.scale_to_length(self.barrel_distance)
        scaled_launch_vector -= rotated_launch_vector
        self.shoot_sound.sound.play()
        for i in range(20):
            self.camera.particle_circle.add_particles(self.rect.center + scaled_launch_vector)
        self.camera.target = self.shell(self.camera, self.stage, self.rect.center + scaled_launch_vector, vector, owner, self.cannon_group)

    def damage(self, damage, is_fire=False):
        if is_fire and self.health - damage <= 0:
            self.fire_turn = 0
        else:
            if self.health > 0:
                self.health -= damage
                if is_fire:
                    self.burning_sound.sound.play()
                Damage(self.camera,
                       (self.rect.centerx + random.randint(-50, 50), self.rect.centery + random.randint(-50, 50)),
                       120, Resources.Fonts.font,
                       20 + 80 * (damage / self.max_health),
                       str(int(damage)),
                       text_color=(255,
                                   255 - [300 * (damage / self.max_health) if 300 * (damage / self.max_health) <= 215 else 215][0],
                                   255 - [300 * (damage / self.max_health) if 300 * (damage / self.max_health) <= 255 else 255][0]))
            if self.health <= 0 and not self.is_death:
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
            self.barrel_move_sound.sound.stop()

    def angle_down(self):
        if self.delta_angle - 1 >= -self.max_delta_angle:
            self.delta_angle -= 1
        else:
            self.delta_angle = -self.max_delta_angle
            self.barrel_move_sound.sound.stop()

    def move_right(self):
        self.direction = "right"
        if self.mobility > 0 and self.incline_angle <= 80:
            dx = 0
            try:
                while not self.stage.mask.get_at((self.rect.centerx + dx, self.rect.centery)):
                    dx += 1

                if 0 <= dx <= 6:
                    pass
                else:
                    self.vector.x = 1
            except:
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
        else:
            self.move_sound.sound.stop()

    def move_left(self):
        self.direction = "left"
        if self.mobility > 0 and self.incline_angle >= -80:
            dx = 0
            try:
                while not self.stage.mask.get_at((self.rect.centerx + dx, self.rect.centery)):
                    dx -= 1

                if -6 <= dx <= 0:
                    pass
                else:
                    self.vector.x = -1
            except:
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
        else:
            self.move_sound.sound.stop()

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
    barrel_texture = Resources.Texture.Cannons.Barrel.basic_barrel
    wheel_texture = Resources.Texture.Cannons.Wheel.basic_wheel
    shell = BasicShell
    shoot_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.shoot)
    damage_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.damage)
    barrel_move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.barrel_move)
    move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.move)
    burning_sound = Sound(all_sounds, Resources.Sounds.Cannon.Basic.burning)
    barrel_length = 85
    barrel_distance = 25

    default_angle = 20
    max_delta_angle = 20
    max_health = 1000
    max_mobility = 1000


class Ballista(Cannon):
    name = "발리스타"
    barrel_texture = Resources.Texture.Cannons.Barrel.ballista_barrel
    wheel_texture = Resources.Texture.Cannons.Wheel.ballista_wheel
    shell = Arrow
    shoot_sound = Sound(all_sounds, Resources.Sounds.Cannon.Ballista.shoot)
    damage_sound = Sound(all_sounds, Resources.Sounds.Cannon.Ballista.damage)
    barrel_move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Ballista.barrel_move)
    move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Ballista.move)
    burning_sound = Sound(all_sounds, Resources.Sounds.Cannon.Ballista.burning)
    barrel_length = 100
    barrel_distance = 30

    default_angle = 20
    max_delta_angle = 40
    max_health = 800
    max_mobility = 2500


class FlameCannon(Cannon):
    name = "화포"
    barrel_texture = Resources.Texture.Cannons.Barrel.flame_cannon_barrel
    wheel_texture = Resources.Texture.Cannons.Wheel.flame_cannon_wheel
    shell = FireBall
    shoot_sound = Sound(all_sounds, Resources.Sounds.Cannon.FlameCannon.shoot)
    damage_sound = Sound(all_sounds, Resources.Sounds.Cannon.FlameCannon.damage)
    barrel_move_sound = Sound(all_sounds, Resources.Sounds.Cannon.FlameCannon.barrel_move)
    move_sound = Sound(all_sounds, Resources.Sounds.Cannon.FlameCannon.move)
    burning_sound = Sound(all_sounds, Resources.Sounds.Cannon.FlameCannon.burning)
    barrel_length = 100
    barrel_distance = 20

    default_angle = 20
    max_delta_angle = 30
    max_health = 1000
    max_mobility = 1000


class Catapult(Cannon):
    name = "캐터펄트"
    barrel_texture = Resources.Texture.Cannons.Barrel.catapult_barrel
    body_texture = Resources.Texture.Cannons.Body.catapult_body
    wheel_texture = Resources.Texture.Cannons.Wheel.catapult_wheel
    shell = Stone
    shoot_sound = Sound(all_sounds, Resources.Sounds.Cannon.Catapult.shoot)
    damage_sound = Sound(all_sounds, Resources.Sounds.Cannon.Catapult.damage)
    barrel_move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Catapult.barrel_move)
    move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Catapult.move)
    burning_sound = Sound(all_sounds, Resources.Sounds.Cannon.Catapult.burning)
    barrel_length = 100
    barrel_distance = 20

    default_angle = 45
    max_delta_angle = 45
    max_health = 1200
    max_mobility = 700

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
        self.fire_turn = 0
        self.fire_effect = None

        self.stage = stage
        self.vector = pygame.math.Vector2(vector)
        self.gravity = stage.gravity

        self.barrel = self.Barrel(self.barrel_texture)
        self.body = self.Body(self.body_texture)
        self.wheel = self.Wheel(self.wheel_texture)
        self.cannon_ui = CannonUI(self)

        self.image = self.blit_cannon()
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft

        self.mask = self.wheel.mask

        self.collide_pos = (0, 0)
        self.screen = pygame.display.get_surface()

    def blit_cannon(self):
        surf = pygame.surface.Surface((200, 200)).convert_alpha()
        surf.fill((0, 0, 0, 0))

        if self.direction == "right":
            self.barrel.blit(surf, (0, 0), self.incline_angle)
            self.body.blit(surf, (0, 0), self.incline_angle)
            self.wheel.blit(surf, (0, 0), self.incline_angle)
        elif self.direction == "left":
            self.barrel.blit(surf, (0, 0), -self.incline_angle)
            self.body.blit(surf, (0, 0), -self.incline_angle)
            surf = pygame.transform.flip(surf, True, False)
            self.wheel.blit(surf, (0, 0), self.incline_angle)

        return surf

    def collide_check(self):
        dy = 0
        self.on_ground = True
        try:
            while not self.stage.mask.get_at((self.rect.centerx, self.rect.centery + dy)):
                dy += 1

            if 0 <= dy <= 18:
                self.rect.centery = (self.rect.centery - 18) + dy
            else:
                self.on_ground = False
        except:
            self.on_ground = False

        if self.on_ground:
            self.vector.y = 0

    def move_right(self):
        self.direction = "right"
        if self.mobility > 0 and self.incline_angle <= 80:
            dx = 0
            try:
                while not self.stage.mask.get_at((self.rect.centerx + dx, self.rect.centery)):
                    dx += 1

                if 0 <= dx <= 6:
                    pass
                else:
                    self.vector.x = 1
            except:
                self.vector.x = 1
            if self.incline_angle >= 0:
                delta_mobility = (6 + abs(self.incline_angle) / 4)
            else:
                delta_mobility = 6
            if self.mobility - delta_mobility >= 0:
                self.mobility -= delta_mobility
            else:
                self.mobility = 0
        else:
            self.move_sound.sound.stop()

    def move_left(self):
        self.direction = "left"
        if self.mobility > 0 and self.incline_angle >= -80:
            dx = 0
            try:
                while not self.stage.mask.get_at((self.rect.centerx + dx, self.rect.centery)):
                    dx -= 1

                if -6 <= dx <= 0:
                    pass
                else:
                    self.vector.x = -1
            except:
                self.vector.x = -1
            if self.incline_angle <= 0:
                delta_mobility = (6 + abs(self.incline_angle) / 4)
            else:
                delta_mobility = 6
            if self.mobility - delta_mobility >= 0:
                self.mobility -= delta_mobility
            else:
                self.mobility = 0
        else:
            self.move_sound.sound.stop()

    class Barrel:
        def __init__(self, texture):
            self.image = load_png(texture)
            self.rect = self.image.get_rect()

        def blit(self, surf, topleft, angle):
            rotated_image = pygame.transform.rotate(self.image, angle)
            new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=topleft).center)

            surf.blit(rotated_image, new_rect)

    class Body:
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

        def blit(self, surf, topleft, angle):
            rotated_image = pygame.transform.rotate(self.image, angle)
            new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=topleft).center)

            surf.blit(rotated_image, new_rect)


class Tank(Cannon):
    name = "탱크"
    barrel_texture = Resources.Texture.Cannons.Barrel.tank_barrel
    body_texture = Resources.Texture.Cannons.Body.tank_body
    wheel_texture = Resources.Texture.Cannons.Wheel.tank_wheel
    shell = Missile
    shoot_sound = Sound(all_sounds, Resources.Sounds.Cannon.Tank.shoot)
    damage_sound = Sound(all_sounds, Resources.Sounds.Cannon.Tank.damage)
    barrel_move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Tank.barrel_move)
    move_sound = Sound(all_sounds, Resources.Sounds.Cannon.Tank.move)
    burning_sound = Sound(all_sounds, Resources.Sounds.Cannon.Tank.burning)
    barrel_length = 100
    barrel_distance = 20

    default_angle = 10
    max_delta_angle = 20
    max_health = 1400
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
        self.fire_turn = 0
        self.fire_effect = None

        self.stage = stage
        self.vector = pygame.math.Vector2(vector)
        self.gravity = stage.gravity

        self.barrel = self.Barrel(self.barrel_texture)
        self.body = self.Body(self.body_texture)
        self.wheel = self.Wheel(self.wheel_texture)
        self.cannon_ui = CannonUI(self)

        self.image = self.blit_cannon()
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft

        self.mask = self.wheel.mask

        self.collide_pos = (0, 0)
        self.screen = pygame.display.get_surface()

    def blit_cannon(self):
        surf = pygame.surface.Surface((200, 200)).convert_alpha()
        surf.fill((0, 0, 0, 0))

        if self.direction == "right":
            vector = pygame.Vector2(
                [-math.cos(math.radians(-self.incline_angle)), -math.sin(math.radians(-self.incline_angle))])
            rotated_launch_vector = vector.copy().rotate(90)
            scaled_launch_vector = vector.copy()
            scaled_launch_vector.scale_to_length(25)
            rotated_launch_vector.scale_to_length(35)
            rotated_launch_vector -= scaled_launch_vector
            self.barrel.blit(surf, (0, 0), self.launch_angle, rotated_launch_vector)
            self.body.blit(surf, (0, 0), self.incline_angle)
            self.wheel.blit(surf, (0, 0), self.incline_angle)
        elif self.direction == "left":
            vector = pygame.Vector2(
                [-math.cos(math.radians(self.incline_angle)), -math.sin(math.radians(self.incline_angle))])
            rotated_launch_vector = vector.copy().rotate(90)
            scaled_launch_vector = vector.copy()
            scaled_launch_vector.scale_to_length(25)
            rotated_launch_vector.scale_to_length(35)
            rotated_launch_vector -= scaled_launch_vector
            self.barrel.blit(surf, (0, 0), self.launch_angle, rotated_launch_vector)
            self.body.blit(surf, (0, 0), -self.incline_angle)
            surf = pygame.transform.flip(surf, True, False)
            self.wheel.blit(surf, (0, 0), self.incline_angle)

        return surf

    def collide_check(self):
        dy = 0
        self.on_ground = True
        try:
            while not self.stage.mask.get_at((self.rect.centerx, self.rect.centery + dy)):
                dy += 1

            if 0 <= dy <= 16:
                self.rect.centery = (self.rect.centery - 16) + dy
            else:
                self.on_ground = False
        except:
            self.on_ground = False

        if self.on_ground:
            self.vector.y = 0

    def move_right(self):
        self.direction = "right"
        if self.mobility > 0 and self.incline_angle <= 80:
            dx = 0
            try:
                while not self.stage.mask.get_at((self.rect.centerx + dx, self.rect.centery)):
                    dx += 1

                if 0 <= dx <= 6:
                    pass
                else:
                    self.vector.x = 1
            except:
                self.vector.x = 1
            if self.incline_angle >= 0:
                delta_mobility = (6 + abs(self.incline_angle) / 4)
            else:
                delta_mobility = 6
            if self.mobility - delta_mobility >= 0:
                self.mobility -= delta_mobility
            else:
                self.mobility = 0
        else:
            self.move_sound.sound.stop()

    def move_left(self):
        self.direction = "left"
        if self.mobility > 0 and self.incline_angle >= -80:
            dx = 0
            try:
                while not self.stage.mask.get_at((self.rect.centerx + dx, self.rect.centery)):
                    dx -= 1

                if -6 <= dx <= 0:
                    pass
                else:
                    self.vector.x = -1
            except:
                self.vector.x = -1
            if self.incline_angle <= 0:
                delta_mobility = (6 + abs(self.incline_angle) / 4)
            else:
                delta_mobility = 6
            if self.mobility - delta_mobility >= 0:
                self.mobility -= delta_mobility
            else:
                self.mobility = 0
        else:
            self.move_sound.sound.stop()

    class Barrel:
        def __init__(self, texture):
            self.image = load_png(texture)
            self.rect = self.image.get_rect()

        def blit(self, surf, topleft, angle, vector):
            new_surf = pygame.surface.Surface((200, 200)).convert_alpha()
            new_surf.fill((0, 0, 0, 0))
            new_surf.blit(self.image, (0, 35))
            rotated_image = pygame.transform.rotate(new_surf, angle)
            new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=topleft).center)

            surf.blit(rotated_image, new_rect.topleft + vector)

    class Body:
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

        def blit(self, surf, topleft, angle):
            rotated_image = pygame.transform.rotate(self.image, angle)
            new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=topleft).center)

            surf.blit(rotated_image, new_rect)


CANNONS = {
    1: BasicCannon,
    2: Ballista,
    3: FlameCannon,
    4: Catapult,
    5: Tank
}