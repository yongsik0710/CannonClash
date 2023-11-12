import pygame
from stage import *
from shell import *


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("대포 게임")

clock = pygame.time.Clock()
FPS = 60

from levels import *
stage_1 = Stage(Levels.level_1, 1, 0)
a = Ball((45, 8))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((100, 100, 100))
    for i in range(9):
        for j in range(16):
            stage_1.level[i][j].update(j * 120, i * 120)
            screen.blit(stage_1.level[i][j].image, stage_1.level[i][j].rect)
    a.update()
    screen.blit(a.image, a.rect)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
