import pygame


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pygame.init()
pygame.display.set_caption("대포 게임")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((100, 100, 100))
    pygame.display.update()

pygame.quit()