import pygame


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
FPS = 60

surf = pygame.surface.Surface((100, 100)).convert_alpha()
surf.fill((0, 0, 0, 0))
pygame.draw.circle(surf, "#00ff00", (50, 50), 50)
level_img = pygame.image.load("level.png").convert_alpha()
ball_img = pygame.image.load("Images/Shells/ball.png")
test_mask = pygame.mask.from_surface(level_img)
ball_mask = pygame.mask.from_surface(ball_img)
circle_mask = pygame.mask.from_surface(surf)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#aaaaaa")
    pos = pygame.mouse.get_pos()

    if pygame.mask.Mask.overlap_area(test_mask, ball_mask, (pos[0] - 16, pos[1] - 16)):
        pygame.mask.Mask.erase(test_mask, circle_mask, (pos[0] - 50, pos[1] - 50))

    a = test_mask.to_surface(setsurface=level_img, unsetcolor=(0, 0, 0, 0))
    screen.blit(a, (0, 0))
    screen.blit(ball_img, (pos[0] - 16, pos[1] - 16))
    pygame.display.update()
