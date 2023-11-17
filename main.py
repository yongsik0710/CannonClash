import pygame
from shell import *
from levels import *
from stage import *


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("대포 게임")

background = pygame.image.load("images/forest.png").convert()

clock = pygame.time.Clock()
FPS = 60

stage_1 = Stage(Levels.level_1, 1.0, 0)
blocks = pygame.sprite.Group(stage_1.level)
non_passable_blocks = pygame.sprite.Group([stage_1.level[y][x] for y in range(18) for x in range(32) if not stage_1.level[y][x].passable])
shell_1 = Shell(stage_1, (300, 500), [8, -12])
projectiles = pygame.sprite.Group(shell_1)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.blit(background, (0, 0))
    blocks.draw(screen)
    projectiles.update()
    projectiles.draw(screen)
    if pygame.sprite.groupcollide(projectiles, non_passable_blocks, False, False):
        test = []
        for block in non_passable_blocks:
            if pygame.sprite.collide_circle(shell_1, block):
                test.append(block)
        shell_1.explode(test, blocks)
        print("충돌함!")

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
