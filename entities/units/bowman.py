from .unit import *

class Bowman(Unit):

    def __init__(self,tile, map):
        super().__init__(tile, map)
        image = pg.image.load("assets/graphics/bowman.png").convert_alpha()
        self.name = "bowman"
        self.image = pg.transform.scale(image, (image.get_width(), image.get_height()))

        self.fieldofview = 4
        self.movingspeed = 8
        self.hp = 30
        self.maxhp = 30
        self.atkdmg = 15
