from blocks import *


class Stage:
    def __init__(self, level, gravity, airResistance):
        self.level = self.loadLevel(level)
        self.gravity = gravity
        self.airResistance = airResistance

    def loadLevel(self, level):
        for y in range(18):
            for x in range(32):
                if level[y][x] == Air.id: level[y][x] = Air(x, y)
                elif level[y][x] == Grass.id: level[y][x] = Grass(x, y)
                elif level[y][x] == Dirt.id: level[y][x] = Dirt(x, y)
                elif level[y][x] == Stone.id: level[y][x] = Stone(x, y)
                elif level[y][x] == Iron.id: level[y][x] = Iron(x, y)
                else: level[y][x] = Block(x, y)
        return level
