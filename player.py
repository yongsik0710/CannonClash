class Player:
    def __init__(self, number):
        self.number = number
        self.name = "player name"
        self.cannon = None
        self.turn = False

    def shoot_shell(self):
        pass

    def next_turn(self):
        self.turn = False

    def process(self):
        pass
