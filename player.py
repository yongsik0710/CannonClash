class Player:
    def __init__(self, cannon):
        self.cannon = cannon
        self.turn = False

    def shoot_shell(self, shell):
        pass

    def next_turn(self):
        self.turn = True
