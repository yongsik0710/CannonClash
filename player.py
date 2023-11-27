class Player:
    def __init__(self, number):
        self.number = number
        self.name = "player name"
        self.cannon_id = 0
        self.cannon = None
        self.turn = False

    def shoot_shell(self, shell):
        pass

    def next_turn(self):
        self.turn = False
