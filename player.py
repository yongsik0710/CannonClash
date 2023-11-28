import pygame


class Player:
    def __init__(self, number):
        self.number = number
        self.name = "player name"
        self.cannon = None
        self.missile_game = None
        self.power = 10

    def shoot_shell(self, vector):
        self.cannon.shoot_shell(vector)

    def process(self, event):
        self.event_check(event)
        # self.next_turn()

    def event_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                cannon_pos = pygame.Vector2(self.cannon.rect.center)
                pos = pygame.Vector2(pygame.mouse.get_pos() + self.missile_game.camera_group.offset)
                vector = pos - cannon_pos
                self.cannon.shoot_shell(vector / 50)
                self.next_turn()

    def next_turn(self):
        self.missile_game.next_turn()
