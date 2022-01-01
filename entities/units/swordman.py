import pygame as pg

from .unit import Unit


class Swordman(Unit):

    def __init__(self,tile, map):
        super().__init__(tile, map)
        image = pg.image.load("assets/graphics/swordman.png").convert_alpha()
        self.name = "swordman"
        self.image = pg.transform.scale(image, (image.get_width(), image.get_height()))

        self.fieldofview = 4
        self.movingspeed = 6
        self.hp = 60
        self.maxhp = 60
        self.atkdmg = 20
