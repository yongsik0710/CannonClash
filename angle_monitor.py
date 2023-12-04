import pygame
import math


class AngleMonitor:
    def __init__(self, surface, x, y, cannon):
        self.surface = surface
        self.cannon = cannon
        self.x = x
        self.y = y

    def draw(self):
        surf = pygame.surface.Surface((200, 200)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        rect = surf.get_rect()
        radius = 100
        pygame.draw.circle(surf, "#f0f0f0", rect.center, radius)
        pygame.draw.circle(surf, "#333333", rect.center, radius * 0.9)

        # 경사각 선 그리기
        angle_vector = self.get_vector(-self.cannon.incline_angle, radius)
        pygame.draw.line(surf, (255, 0, 0), rect.center, rect.center + angle_vector)
        pygame.draw.line(surf, (255, 0, 0), rect.center, rect.center - angle_vector)

        # 발사가능한 각 그리기
        max_angle = self.cannon.incline_angle + self.cannon.max_delta_angle
        min_angle = self.cannon.incline_angle - self.cannon.max_delta_angle

        if self.cannon.direction == "right":
            angle_vector = self.get_vector(-max_angle, radius)
            pygame.draw.line(surf, (255, 255, 0), rect.center, rect.center + angle_vector)
            angle_vector = self.get_vector(-min_angle, radius)
            pygame.draw.line(surf, (255, 255, 0), rect.center, rect.center + angle_vector)
        else:
            angle_vector = self.get_vector(-max_angle, radius)
            pygame.draw.line(surf, (255, 255, 0), rect.center, rect.center - angle_vector)
            angle_vector = self.get_vector(-min_angle, radius)
            pygame.draw.line(surf, (255, 255, 0), rect.center, rect.center - angle_vector)

        # 현재 발사각 그리기
        if self.cannon.direction == "right":
            angle_vector = self.get_vector(-self.cannon.launch_angle, radius)
            pygame.draw.line(surf, (0, 255, 0), rect.center, rect.center + angle_vector)
        else:
            angle_vector = self.get_vector(self.cannon.launch_angle, radius)
            pygame.draw.line(surf, (0, 255, 0), rect.center, rect.center - angle_vector)

        # 수평선 그리기
        angle_vector = self.get_vector(0.0, radius)
        pygame.draw.line(surf, (255, 255, 255), rect.center, rect.center + angle_vector, 2)
        pygame.draw.line(surf, (255, 255, 255), rect.center, rect.center - angle_vector, 2)

        pygame.draw.circle(surf, "#808080", rect.center, radius * 0.1)

        self.surface.blit(surf, (self.x, self.y))

    def get_vector(self, angle, radius):
        vector = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle)))
        vector.scale_to_length(radius * 0.9)

        return vector
