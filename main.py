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


def main_menu():
    font = pygame.font.Font(None, 60)
    play_button = Button(screen, 790, 700, 400, 100, 5, font, "Play")

    running = True
    while running:
        screen.fill("#f0f0f0")
        if play_button.draw():
            game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

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
                    if not game_menu():
                        running = False

        Game.process()

        pygame.display.update()
        clock.tick(FPS)


def game_menu():
    font = pygame.font.Font(None, 60)
    resume_button = Button(screen, 790, 700, 400, 100, 5, font, "Resume")
    back_to_main_menu = Button(screen, 790, 820, 400, 100, 5, font, "Back to Main Menu")

    running = True
    while running:
        screen.fill("#ffffff")
        if resume_button.draw():
            running = False
        if back_to_main_menu.draw():
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(FPS)


main_menu()
