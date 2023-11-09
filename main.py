import pygame
from stage import *
from config import *
from shell import *


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("대포 게임")

clock = pygame.time.Clock()
FPS = 165

a = Ball((45, 10))
all_sprites = pygame.sprite.Group(a)


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
            if i <= 5:
                screen.blit(Texture.air, [120 * j, 120 * i])
            elif i == 6:
                screen.blit(Texture.grass, [120 * j, 120 * i])
            elif i == 7:
                screen.blit(Texture.dirt, [120 * j, 120 * i])
            else:
                screen.blit(Texture.stone, [120 * j, 120 * i])
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
