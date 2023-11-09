from config import *


class Block:
    health = 100
    blastResistance = 0
    passable = False
    texture = ""
    layer = ""


class Air(Block):
    blastResistance = 0
    passable = True


class Grass(Block):
    blastResistance = 0


class Dirt(Block):
    blastResistance = 0


class Stone(Block):
    blastResistance = 30


class Iron(Block):
    blastResistance = 70
