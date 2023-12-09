import pygame, sys, random


class ParticlePrinciple:
    def __init__(self):
        self.particles = []

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(screen, pygame.Color('White'), particle[0], int(particle[1]))

    def add_particles(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        radius = 10
        direction_x = random.randint(-30, 30) / 10
        direction_y = random.randint(-30, 30) / 10
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy


class ParticleNyan:
    def __init__(self):
        self.particles = []
        self.size = 12

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x -= 1
                pygame.draw.rect(screen, particle[1], particle[0])

        self.draw_nyancat()

    def add_particles(self, offset, color):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1] + offset
        particle_rect = pygame.Rect(int(pos_x - self.size / 2), int(pos_y - self.size / 2), self.size, self.size)
        self.particles.append((particle_rect, color))

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[0].x > 0]
        self.particles = particle_copy

    def draw_nyancat(self):
        nyan_rect = nyan_surface.get_rect(center=pygame.mouse.get_pos())
        screen.blit(nyan_surface, nyan_rect)


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


pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

particle1 = ParticlePrinciple()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == PARTICLE_EVENT:
            for i in range(20):
                particle1.add_particles()
            # particle2.add_particles(-30,pygame.Color("Red"))
            # particle2.add_particles(-18,pygame.Color("Orange"))
            # particle2.add_particles(-6,pygame.Color("Yellow"))
            # particle2.add_particles(6,pygame.Color("Green"))
            # particle2.add_particles(18,pygame.Color("Blue"))
            # particle2.add_particles(30,pygame.Color("Purple"))

    screen.fill((30, 30, 30))
    particle1.emit()
    # particle2.emit()
    pygame.display.update()
    clock.tick(120)
