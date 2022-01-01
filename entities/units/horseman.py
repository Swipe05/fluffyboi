from .unit import *

class Horseman(Unit):

    def __init__(self,tile, map):
        super().__init__(tile, map)
        image = pg.image.load("assets/graphics/horseman.png").convert_alpha()
        self.name = "horseman"
        self.image = pg.transform.scale(image, (image.get_width(), image.get_height()))
        
        self.fieldofview = 5
        self.movingspeed = 12
        self.hp = 50
        self.maxhp = 50
        self.atkdmg = 25
