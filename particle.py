import pygame


class ParticleStar:
    def __init__(self):
        self.particles = []
        self.surface = pygame.image.load('Star.png').convert_alpha()
        self.width = self.surface.get_rect().width
        self.height = self.surface.get_rect().height

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x += particle[1]
                particle[0].y += particle[2]
                particle[3] -= 0.2
                screen.blit(self.surface, particle[0])

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