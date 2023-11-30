import pygame


class Player:
    def __init__(self, number):
        self.number = number
        self.name = "player name"
        self.cannon = None
        self.missile_game = None
        self.power = 0

    def shoot_shell(self):
        self.cannon.shoot_shell(self.power)

    def process(self):
        pass

    def next_turn(self):
        self.missile_game.next_turn()
