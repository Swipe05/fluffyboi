import pygame as pg

class Building:
    def __init__(self, pos, resource_manager, map=None, team=1):
        self.team = team
        self.pos = pos
        self.resource_manager = resource_manager
        self.fieldofview = 5
        self.in_construction = False
        self.construc_cooldown = pg.time.get_ticks()
        self.construc_time = 3 # 3*game_speed
        if map:
            self.map = map
            self.update_vision_matrix = map.update_vision_matrix(self.pos, self.fieldofview)

    
    def update(self):
        now = pg.time.get_ticks()
        if self.in_construction :
            if now - self.construc_cooldown > self.construc_time*self.map.GAME_SPEED :
                #self.map.buildings[self.pos[0]][self.pos[1]] = self
                self.update_vision_matrix
                self.in_construction = False
                self.construc_cooldown = now