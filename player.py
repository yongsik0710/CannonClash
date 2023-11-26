class Player:
    def __init__(self, name, cannon):
        self.name = name
        self.number = 0
        self.cannon = cannon
        self.turn = False

    def shoot_shell(self, shell):
        pass

    def next_turn(self):
        self.turn = False
