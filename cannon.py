from shell import *
import pygame
import os
import math


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("Images", name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (240, 240))
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

    def __init__(self, group, stage, pos, vector):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.max_health = 1000
        self.health = self.max_health
        self.angle = 0.0
        self.delta_angle = 0.0
        self.on_ground = False
        self.direction = "right"

        self.stage = stage
        self.vector = pygame.math.Vector2(vector)
        self.gravity = stage.gravity

        self.barrel = self.Barrel(self.barrel_texture)
        self.wheel = self.Wheel(self.wheel_texture)

        self.image = self.draw_cannon()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

        self.mask = self.wheel.mask

        self.collide_pos = (0, 0)
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()

    def draw_cannon(self):
        surf = pygame.surface.Surface((240, 240)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        if self.direction == "right":
            self.barrel.draw(surf, (0, 0), self.angle - 20 + self.delta_angle)
            self.wheel.draw(surf, (0, 0))
        elif self.direction == "left":
            self.barrel.draw(surf, (0, 0), -self.angle - 20 + self.delta_angle)
            surf = pygame.transform.flip(surf, True, False)
            self.wheel.draw(surf, (0, 0))
        return surf

    def update(self):
        if not self.on_ground:
            self.vector.y += self.gravity / 5
        self.collide_check()

        surf = pygame.surface.Surface((50, 50)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        surf.blit(self.stage.image,
                  (-(self.rect.centerx - 25), -(self.rect.centery)))
        mask = pygame.mask.from_surface(surf)

        b = []
        for x in range(50):
            for y in range(40):
                if mask.get_at((x, y)):
                    b.append((x, y))
                    break

        c = [0, 0]
        for i in range(len(b)):
            c[0] += b[i][0] - b[0][0]
            c[1] += b[i][1] - b[0][1]

        try:
            # pygame.draw.line(surf, (255, 255, 0), b[0], (b[0][0] + c[0], b[0][1] + c[1]), 1)
            self.angle = pygame.Vector2((b[0][0] + c[0] - b[0][0], b[0][1] + c[1] - b[0][1])).angle_to((0, 0))
        except:
            pass

        self.image = self.draw_cannon()
        self.rect = self.rect.move(self.vector)

    def collide_check(self):
        if pygame.sprite.collide_mask(self, self.stage):
            self.on_ground = True
            if self.mask.overlap(self.stage.mask, (-self.rect.x, -self.rect.y + 3)):
                self.vector.y = -2
            else:
                self.collide_pos = self.mask.overlap(self.stage.mask, (-self.rect.x, -self.rect.y))
                self.collide_pos = (self.collide_pos[0] + self.rect.x, self.collide_pos[1] + self.rect.y)
                self.vector.y = 0
        else:
            self.on_ground = False

    def shoot_shell(self, power):
        if self.direction == "right":
            vector = pygame.Vector2([math.cos(math.radians(self.angle)), - math.sin(math.radians(self.angle))])
            vector.scale_to_length(power / 3)
            vector2 = vector.copy()
            vector3 = vector.copy()
            vector3.scale_to_length(70)
            vector2 = vector2.rotate(90)
            vector2.scale_to_length(45)
            vector2 = vector2 - vector3
            self.shell(self.camera, self.stage, self.rect.center - vector2, vector)
        else:
            vector = pygame.Vector2([- math.cos(math.radians(-self.angle)), - math.sin(math.radians(-self.angle))])
            vector.scale_to_length(power / 3)
            vector2 = vector.copy()
            vector3 = vector.copy()
            vector3.scale_to_length(70)
            vector2 = vector2.rotate(-90)
            vector2.scale_to_length(45)
            vector2 = vector2 - vector3
            self.shell(self.camera, self.stage, self.rect.center - vector2, vector)


    def move_right(self):
        self.direction = "right"
        self.rect = self.rect.move(1, 0)
        self.wheel.roll_cw()

    def move_left(self):
        self.direction = "left"
        self.rect = self.rect.move(-1, 0)
        self.wheel.roll_acw()

    class Barrel:
        def __init__(self, texture):
            self.image = load_png(texture)
            self.rect = self.image.get_rect()

        def draw(self, surf, topleft, angle):
            rotated_image = pygame.transform.rotate(self.image, angle)
            new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=topleft).center)

            surf.blit(rotated_image, new_rect)

    class Wheel:
        def __init__(self, texture):
            self.image = load_png(texture)
            self.mask = pygame.mask.from_surface(self.image)
            self.angle = 0.0

        def draw(self, surf, topleft):
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=topleft).center)

            surf.blit(rotated_image, new_rect)

        def roll_cw(self):
            self.angle -= 2

        def roll_acw(self):
            self.angle += 2


class BasicCannon(Cannon):
    name = "Basic"
    barrel_texture = TexturePath.Cannon.Barrel.barrel_1
    wheel_texture = TexturePath.Cannon.Wheel.wheel_1
    shell = BasicShell


class TestCannon(Cannon):
    name = "Test"
    barrel_texture = TexturePath.Cannon.Barrel.barrel_2
    wheel_texture = TexturePath.Cannon.Wheel.wheel_2
    shell = Shell


CANNONS = {
    1: BasicCannon,
    2: TestCannon
}