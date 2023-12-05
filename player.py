from player_ui import *


class Player:
    def __init__(self, number):
        self.number = number
        self.name = "player name"
        self.cannon = None
        self.missile_game = None
        self.player_ui = None
        self.turn = False
        self.is_death = False
        self.max_power = 180
        self.power = 0

    def death(self):
        self.turn = False
        self.is_death = True
        self.next_turn()

    def init_player_ui(self):
        self.player_ui = PlayerUI(self)

    def shoot_shell(self):
        if self.power <= self.max_power:
            self.cannon.shoot_shell(self.power, self)
        else:
            self.cannon.shoot_shell(self.max_power, self)
        self.player_ui.power_bar.prev_power = self.power
        self.power = 0
        self.turn = False

    def next_turn(self):
        self.missile_game.next_turn()

    def skip(self):
        self.missile_game.next_turn()

    def draw_player_ui(self):
        self.player_ui.update()
        self.player_ui.draw()

