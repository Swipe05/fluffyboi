import pygame as pg
import sys
from .map import Map
from utils.settings import *
from utils.util_functions import draw_text,spawn_enemy_unit,spawn_ally_unit
from .camera import Camera
from .hud import Hud
from .resource_manager import ResourceManager
from entities.units.worker import Herobrine
from .display import Display


class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.cheat = CHEAT
        self.mapsize = WORLD_SIZE

        # entities
        self.entities = []

        # resource manager
        self.resource_manager = ResourceManager()

        # hud
        self.hud = Hud(self.resource_manager, self.width, self.height)


        # camera
        self.camera = Camera(self.width, self.height)
        self.camera.scroll.x = -int(31.6*WORLD_SIZE - 600)
        self.camera.scroll.y = WORLD_SIZE
    def initiate_map(self):
        # Map
        self.map = Map(
             self.resource_manager, self.entities, self.hud,
            self.mapsize, self.width, self.height
        )
    def initiate_display(self):
        # Display
        self.display = Display(
            self.screen,self.clock,self.entities,
            self.resource_manager,self.hud,self.map,self.camera
        )




    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            if self.events():
                self.playing=False
                return True
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return True
                if self.cheat:
                    if event.key == pg.K_F1:
                        spawn_ally_unit(self,Herobrine)

                    if event.key == pg.K_F2:
                        for n in self.resource_manager.resources:
                            self.resource_manager.resources[n] +=10000

                    if event.key == pg.K_F3:
                        for n in self.resource_manager.resources:
                            if self.resource_manager.resources[n]-10000>=0:
                                self.resource_manager.resources[n] -=10000
                            else: self.resource_manager.resources[n]=0

                    if event.key == pg.K_F4:
                        for i in range(len(GAME_SPEED)):
                            if self.map.GAME_SPEED==GAME_SPEED[i]:
                                x=i
                        if x < len(GAME_SPEED)-1:
                            self.map.GAME_SPEED=GAME_SPEED[x+1]
                        else: self.map.GAME_SPEED=GAME_SPEED[0]

                    if event.key == pg.K_F5:
                        vision_range = range(len(self.map.vision_matrix))
                        for x in vision_range:
                            self.map.vision_matrix[x] = [1] * len(self.map.vision_matrix[x])

                    if event.key == pg.K_F6:
                        vision_range = range(len(self.map.vision_matrix))
                        for x in vision_range:
                            self.map.vision_matrix[x] = [0] * len(self.map.vision_matrix[x])
                        for x in range(len(self.map.buildings)):
                            for y in range(len(self.map.buildings)):
                                if self.map.buildings[x][y] is not None and self.map.buildings[x][y].team==1:
                                    self.map.update_vision_matrix((x,y),self.map.buildings[x][y].fieldofview)
            # if event.type == pg.MOUSEBUTTONDOWN:

    def update(self):
        self.camera.update()
        for e in self.entities: e.update()
        self.hud.update()
        self.map.update(self.camera)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.display.draw()
        self.hud.draw(self.screen)

        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255, 255, 255),
            (10, 1)
        )
        if self.cheat:
            draw_text(self.screen,"Cheats ON",25,(255, 255, 255),(75, 1))
            draw_text(self.screen,"F1 Herobrine | ",25,(255, 255, 255),(10, 20))
            draw_text(self.screen,"F2-F3 +-10k resources | ",25,(255, 255, 255),(130, 20))
            draw_text(self.screen,"F4 Game speed : " + GAME_SPEED_NAMES[self.map.GAME_SPEED] + " | ",25,(255, 255, 255),(320, 20))
            draw_text(self.screen,"F5 No fog | ",25,(255, 255, 255),(555, 20))
            draw_text(self.screen,"F6 Reset fog | ",25,(255, 255, 255),(645, 20))

        pg.display.flip()

