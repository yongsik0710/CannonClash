import pygame
import random


class Particle:
    class Circle:
        def __init__(self, surface):
            self.particles = []
            self.surface = surface

        def emit(self, offset):
            if self.particles:
                self.delete_particles()
                for particle in self.particles:
                    particle[0][0] += particle[2][0]
                    particle[0][1] += particle[2][1]
                    particle[1] -= 0.4
                    pygame.draw.circle(self.surface, "#575757", particle[0] - offset, int(particle[1]))

        def add_particles(self, pos):
            radius = 10
            direction_x = random.randint(-60, 60) / 10
            direction_y = random.randint(-60, 60) / 10
            particle_circle = [[pos[0], pos[1]], radius, [direction_x, direction_y]]
            self.particles.append(particle_circle)

        def delete_particles(self):
            particle_copy = [particle for particle in self.particles if particle[1] > 0]
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
