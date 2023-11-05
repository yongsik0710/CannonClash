class Block:
    health = 100
    blastResistance = 0
    texture = ""
    layer = ""

    def refresh(self):
        if 80 < self.health <= 100: self.layer = 0
        elif 60 < self.health <= 80: self.layer = 1
        elif 40 < self.health <= 60: self.layer = 2
        elif 20 < self.health <= 40: self.layer = 3
        elif 0 < self.health <= 20: self.layer = 4
        else: pass

    def hit(self, blastDamage):
        self.health -= blastDamage * ((100 - self.blastResistance) / 100)


class Fluid:
    pass


class Air(Fluid):
    pass


class Grass(Block):
    blastResistance = 0


class Dirt(Block):
    blastResistance = 0


class Stone(Block):
    blastResistance = 30


class Iron(Block):
    blastResistance = 70
