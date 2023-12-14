import pygame
import random
from config import *


class Particle:
    class Smoke:
        def __init__(self, surface):
            self.particles = []
            self.screen = surface

        def emit(self, offset):
            if self.particles:
                self.delete_particles()
                for particle in self.particles:
                    particle["pos"][0] += particle["vector"][0]
                    particle["pos"][1] += particle["vector"][1]
                    particle["lifetime"] -= 0.3
                    particle["radius"] -= 0.3
                    pygame.draw.circle(self.screen, particle["color"], particle["pos"] - offset, int(particle["radius"]))

        def add_particles(self, pos):
            radius = 10
            direction_x = random.randint(-60, 60) / 10
            direction_y = random.randint(-60, 60) / 10
            lifetime = 10
            bright = random.randint(80, 120)
            color = [bright, bright, bright]
            particle = {"pos": [pos[0], pos[1]],
                        "vector": [direction_x, direction_y],
                        "lifetime": lifetime,
                        "radius": radius,
                        "color": color}
            self.particles.append(particle)

        def summon_particles(self, pos, noise, count):
            for _ in range(count):
                pos[0] + random.randint(-noise, noise)
                pos[1] - random.randint(-noise, noise)
                self.add_particles(pos)

        def delete_particles(self):
            particle_copy = [particle for particle in self.particles if particle["lifetime"] > 0]
            self.particles = particle_copy

    class Destroy:
        def __init__(self, surface):
            self.particles = []
            self.screen = surface

        def emit(self, offset):
            if self.particles:
                self.delete_particles()
                for particle in self.particles:
                    particle["vector"][1] += 0.2
                    particle["pos"][0] += particle["vector"][0]
                    particle["pos"][1] += particle["vector"][1]
                    particle["lifetime"] -= 0.02
                    if particle["rot_direction"] > 0:
                        particle["rot"] += 11
                    else:
                        particle["rot"] -= 11
                    surf = pygame.surface.Surface((particle["scale"], particle["scale"])).convert_alpha()
                    surf.fill(particle["color"] + [100 + 155 * particle["lifetime"]])
                    rotated_surf = pygame.transform.rotate(surf, particle["rot"])
                    rotated_rect = rotated_surf.get_rect(center=surf.get_rect(center=particle["pos"] - offset).center)
                    self.screen.blit(rotated_surf, rotated_rect)

        def add_particles(self, pos):
            direction_x = random.randint(-100, 100) / 10
            direction_y = random.randint(-80, 50) / 10
            lifetime = 1
            rot = random.randint(0, 180)
            rot_direction = random.choice([-1, 1])
            scale = 10 * (random.randint(50, 100) / 100)
            bright = random.randint(0, 50)
            color = [20 + bright, 20 + bright, 20 + bright]
            particle = {"pos": [pos[0], pos[1]],
                        "vector": [direction_x, direction_y],
                        "lifetime": lifetime,
                        "rot": rot,
                        "rot_direction": rot_direction,
                        "scale": scale,
                        "color": color}
            self.particles.append(particle)

        def summon_particles(self, pos, noise, count):
            for _ in range(count):
                pos[0] + random.randint(-noise, noise)
                pos[1] - random.randint(-noise, noise)
                self.add_particles(pos)

        def delete_particles(self):
            particle_copy = [particle for particle in self.particles if particle["lifetime"] > 0]
            self.particles = particle_copy

    class Flame:
        def __init__(self, surface):
            self.particles = []
            self.screen = surface

        def emit(self, offset):
            if self.particles:
                self.delete_particles()
                for particle in self.particles:
                    particle["pos"][0] += particle["vector"][0]
                    particle["pos"][1] += particle["vector"][1]
                    if particle["lifetime"] - 0.2 >= 0:
                        particle["lifetime"] -= 0.2
                    else:
                        particle["lifetime"] = 0

                    if particle["color"][1] - 4 > 0:
                        particle["color"][1] -= 4
                    if particle["color"][2] - 3 > 0:
                        particle["color"][2] -= 3
                    particle["scale"] = particle["max_scale"] * (particle["lifetime"] / particle["max_lifetime"])

                    surf = pygame.surface.Surface((particle["scale"], particle["scale"])).convert_alpha()
                    surf.fill(particle["color"] + [200 + 55 * (particle["lifetime"] / particle["max_lifetime"])])
                    rotated_surf = pygame.transform.rotate(surf, particle["rot"])
                    rotated_rect = rotated_surf.get_rect(center=surf.get_rect(center=particle["pos"] - offset).center)
                    self.screen.blit(rotated_surf, rotated_rect)

        def add_particles(self, pos):
            direction_x = random.randint(-60, 60) / 10
            direction_y = random.randint(-60, 60) / 10
            lifetime = random.randint(8, 10)
            rot = random.randint(0, 180)
            scale = 25 * (random.randint(60, 100) / 100)
            color = [255, 200, 80]
            self.particles.append({"pos": [pos[0], pos[1]],
                                   "vector": [direction_x, direction_y],
                                   "lifetime": lifetime,
                                   "max_lifetime": lifetime,
                                   "rot": rot,
                                   "scale": scale,
                                   "max_scale": scale,
                                   "color": color})

        def summon_particles(self, pos, noise, count):
            for _ in range(count):
                pos[0] + random.randint(-noise, noise)
                pos[1] - random.randint(-noise, noise)
                self.add_particles(pos)

        def delete_particles(self):
            particle_copy = [particle for particle in self.particles if particle["lifetime"] > 0]
            self.particles = particle_copy

    class ParticleStar:
        def __init__(self):
            self.particles = []
            self.surface = pygame.image.load('Star.png').convert_alpha()
            self.width = self.surface.get_rect().width
            self.height = self.surface.get_rect().height
            self.screen = pygame.display.get_surface()

        def emit(self):
            if self.particles:
                self.delete_particles()
                for particle in self.particles:
                    particle[0].x += particle[1]
                    particle[0].y += particle[2]
                    particle[3] -= 0.2
                    self.screen.blit(self.surface, particle[0])

        def add_particles(self):
            pos_x = pygame.mouse.get_pos()[0] - self.width / 2
            pos_y = pygame.mouse.get_pos()[1] - self.height / 2
            direction_x = random.randint(-3, 3)
            direction_y = random.randint(-3, 3)
            lifetime = random.randint(4, 10)
            particle_rect = pygame.Rect(int(pos_x), int(pos_y), self.width, self.height)
            self.particles.append([particle_rect, direction_x, direction_y, lifetime])

        def delete_particles(self):
            particle_copy = [particle for particle in self.particles if particle[3] > 0]
            self.particles = particle_copy
