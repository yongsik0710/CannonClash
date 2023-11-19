import pygame
from levels import *
from stage import *
from missile_game import *
from button import *


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("대포 게임")
clock = pygame.time.Clock()
FPS = 60

Game = MissileGame(screen, Stage(Levels.level_1, 1.0, 0.0))

button_image = pygame.image.load(Texture.Buttons.button).convert_alpha()


def test():
    print("hi")
    game()


def main_menu():
    click = False
    font = pygame.font.SysFont('Arial', 40)
    play_button = Button(500, 100, button_image, 1)

    running = True
    while running:
        screen.fill((0, 0, 0))
        if play_button.draw(screen) and click:
            game()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(FPS)


def stage_select():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(FPS)


def game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        Game.process()

        pygame.display.update()
        clock.tick(FPS)


main_menu()
