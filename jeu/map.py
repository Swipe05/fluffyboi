import pygame as pg
import random
import noise
import time

from utils.sprite import dict_buildings, dict_workers
from utils.util_functions import draw_text
from utils.settings import *
from utils.save import *

from entities.buildings import Archery_range, Armory, Barrack, EnemyTH, Farm, GoodTH, Mason, Sawmill, Stable
from entities.units import Bowman, Horseman, Swordman, Worker



class Map:

    def __init__(self,  resource_manager, entities, hud, mapsize, width, height,a=3):
        self.resource_manager = resource_manager
        self.entities = entities
        self.hud = hud
        self.mapsize = mapsize
        self.width = width
        self.height = height

        self.perlin_scale = mapsize / 2
        self.GAME_SPEED = GAME_SPEED[2]

        #self.grass_tiles = pg.Surface(
        #    (mapsize * TILE_SIZE * 2, mapsize * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()

        self.grass_tiles = (mapsize * TILE_SIZE * 2, mapsize * TILE_SIZE + 2 * TILE_SIZE)
        self.grass_tiles_width = self.grass_tiles[0]
        self.grass_tiles_length = self.grass_tiles[1]



        if 0: self.load_save() # mettre à 0 pour désactiver l'auto_save
        else:
            self.map = self.create_map()
            self.buildings = [[None for x in range(self.mapsize)] for y in range(self.mapsize)]

        self.vision_matrix = self.create_vision_matrix()
        self.mixed_matrix = self.create_mixed_matrix()

        
 # contains both collision and water tiles

        
        self.workers = [[None for x in range(self.mapsize)] for y in range(self.mapsize)]

        global x1,y1 # GoodTH position
        x1,y1=self.mapsize/2,self.mapsize/2
         # using mixed_matrix
         # to place TH and have empty tiles around to spawn troops
         # Can be extended if we want more visibility
        while ((self.mapsize-self.mapsize/5 > x1 > self.mapsize/5) 
            or (self.mapsize-self.mapsize/5 > y1 > self.mapsize/5)
            # for GoodTH
            or not(self.mixed_matrix[x1][y1] and self.mixed_matrix[x1][y1+1] and
            self.mixed_matrix[x1-1][y1+1] and self.mixed_matrix[x1+1][y1+1] and self.mixed_matrix[x1][y1-2]
           # for EnnemyTH
            and self.mixed_matrix[self.mapsize-x1][self.mapsize-y1] and self.mixed_matrix[self.mapsize-x1][self.mapsize-y1+1] and
            self.mixed_matrix[self.mapsize-x1-1][self.mapsize-y1+1] and self.mixed_matrix[self.mapsize-x1+1][self.mapsize-y1+1] 
            and self.mixed_matrix[self.mapsize-x1][self.mapsize-y1-2])):
           
            x1,y1 = random.randint(3,10),random.randint(3,10)

        #GoodTH
        self.goodTH_x = x1
        self.goodTH_y = y1    
        render_pos = self.map[x1][y1]["render_pos"]
        ent = GoodTH(render_pos, self.resource_manager)
        self.entities.append(ent)
        self.buildings[x1][y1] = ent
        self.update_mixed_matrix(x1,y1)
        self.update_vision_matrix((x1,y1),ent.fieldofview)

        #EnnemyTH
        render_pos = self.map[self.mapsize-x1][self.mapsize-y1]["render_pos"]
        ent = EnemyTH(render_pos, self.resource_manager)  
        self.entities.append(ent)
        self.buildings[self.mapsize-x1][self.mapsize-y1] = ent
        self.update_mixed_matrix(self.mapsize-x1, self.mapsize-y1)

        # self.collision_matrix = self.create_collision_matrix()
        # self.water_matrix = self.create_water_matrix()
        
        # examined tiles and troops after a left click
        self.temp_tile = None
        self.examine_tile = None
        self.examine_troop = None

        # to know if we are placing a building. If this is the case, we can't examine a tile
        self.placing_building = False
        

    def update(self, camera):
        
        mouse_pos = pg.mouse.get_pos()
        global mouse_action
        mouse_action = pg.mouse.get_pressed()
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

        if -1<grid_pos[0]<self.mapsize and -1<grid_pos[1]<self.mapsize:

            if mouse_action[2]: # right click, cancel the selection
                self.examine_tile = None
                self.examine_troop = None
                self.hud.examined_tile = None
                self.hud.examined_troop = None
                self.placing_building = False
                
            # creating troops
            if self.hud.creerworker:
                aworker = Worker(self.map[x1][y1+1], self)
                self.workers.append(aworker)
                self.map[x1][y1+1]["troop"] = True
                time.sleep(.1)
            
            if self.hud.creerswordman:
                aswordman = Swordman(self.map[x1-1][y1+1], self)  
                self.workers.append(aswordman)
                self.map[x1-1][y1+1]["troop"] = True
                time.sleep(.1)
            
            if self.hud.creerbowman:
                abowman = Bowman(self.map[x1+1][y1+1], self)   
                self.workers.append(abowman)
                self.map[x1+1][y1+1]["troop"] = True
                time.sleep(.1)

            if self.hud.creerhorseman:
                ahorseman = Horseman(self.map[x1][y1-2], self)  
                self.workers.append(ahorseman)
                self.map[x1][y1-2]["troop"] = True
                time.sleep(.1)

            if mouse_action[0] and (self.workers[grid_pos[0]][grid_pos[1]] is not None) \
            and self.examine_troop is None and not self.placing_building: # left clicking on a worker to examine it
                
                self.examine_troop=self.workers[grid_pos[0]][grid_pos[1]]
                self.examine_troop_tile=(grid_pos[0],grid_pos[1])             
                time.sleep(.1)

            
            if self.examine_troop is not None: # selected worker's actions on left click
                if self.examine_troop.hp<=0: # unselecting a dead unit
                    self.examine_troop,self.hud.examined_troop = None,None
                if mouse_action[0] and self.buildings[grid_pos[0]][grid_pos[1]] is None:
                    #moving
                    if not (self.map[grid_pos[0]][grid_pos[1]]["collision"] or self.map[grid_pos[0]][grid_pos[1]]["water"]) and self.workers[grid_pos[0]][grid_pos[1]] is None:
                        self.examine_troop.set_destination(self.map[grid_pos[0]][grid_pos[1]])
                        self.examine_troop.create_path()

                    # mining/going to a bloc
                    elif self.map[grid_pos[0]][grid_pos[1]]["collision"]: 
                        if self.map[grid_pos[0]][grid_pos[1]]["resources"]!=0 and self.examine_troop.name=="worker" or self.examine_troop.name=="herobrine":
                            self.examine_troop.mine_tile = self.map[grid_pos[0]][grid_pos[1]]
                        else: self.examine_troop.go_close(self.map[grid_pos[0]][grid_pos[1]])

                    # attacking
                    elif self.workers[grid_pos[0]][grid_pos[1]] is not None and self.workers[grid_pos[0]][grid_pos[1]]!=self.examine_troop:
                        self.examine_troop.attacked_unit = self.workers[grid_pos[0]][grid_pos[1]]

                            

            self.temp_tile = None

            if self.hud.selected_tile is not None: # selecting a building from hud
                self.hud.examined_troop, self.examine_troop = None,None

                if self.can_place_tile(grid_pos):
                    
                    self.placing_building = True


                    render_pos = self.map[grid_pos[0]][grid_pos[1]]["render_pos"]
                    iso_poly = self.map[grid_pos[0]][grid_pos[1]]["iso_poly"]
                    collision = self.map[grid_pos[0]][grid_pos[1]]["collision"]
                    water = self.map[grid_pos[0]][grid_pos[1]]["water"]
                    troop = self.map[grid_pos[0]][grid_pos[1]]["troop"]
                    grid = self.map[grid_pos[0]][grid_pos[1]]["grid"]

                    self.temp_tile = {
                        #"image": img,
                        "render_pos": render_pos,
                        "iso_poly": iso_poly,
                        "collision": collision,
                        "water": water,
                        "troop" : troop,
                        "grid" : grid
                    }
                    # placing buildings
                    if mouse_action[0] and not collision and not water and not troop: # valid tile
                        self.placing_building = True
                        if self.hud.selected_tile["name"] == "Sawmill":
                            ent = Sawmill(grid_pos, self.resource_manage, self)
                            ent.in_construction = True
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Mason":
                            ent = Mason(grid_pos, self.resource_manager, self)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Farm":
                            ent = Farm(grid_pos, self.resource_manager, self)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Town Hall":
                            ent = GoodTH(grid_pos, self.resource_manager)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Enemy Town Hall":
                            ent = EnemyTH(grid_pos, self.resource_manager)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Barrack":
                            ent = Barrack(grid_pos, self.resource_manager, self)
                            ent.in_construction = True
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Archery range":
                            ent = Archery_range(grid_pos, self.resource_manager, self)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Stable":
                            ent = Stable(grid_pos, self.resource_manager, self)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Armory":
                            ent = Armory(grid_pos, self.resource_manager, self)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)

                        ent.in_construction = True
                        self.map[grid_pos[0]][grid_pos[1]]["collision"] = True # adding collision on map
                        self.mixed_matrix[grid_pos[1]][grid_pos[0]] = 0 # adding collision on mixed_matrix
                        #self.collision_matrix[grid_pos[1]][grid_pos[0]] = 0
                        self.hud.selected_tile = None # reset the selection
                        self.placing_building = False


            else: # not selecting an object from hud
                if self.can_place_tile(grid_pos) and not self.placing_building:
                    building = self.buildings[grid_pos[0]][grid_pos[1]]
                    worker = self.workers[grid_pos[0]][grid_pos[1]]
                    if mouse_action[0] and (building is not None): # examinating a building
                        self.examine_tile = grid_pos
                        self.hud.examined_tile = building
                        self.hud.examined_troop = None
                        self.examine_troop = None
                    if mouse_action[0] and (worker is not None): # examinating a worker
                        self.examine_troop_tile = grid_pos
                        self.hud.examined_troop = self.examine_troop
                        self.hud.examined_tile = None
                



    def create_map(self):

        map = []
        r_noise = random.randint(20,40)

        for grid_x in range(self.mapsize):
            map.append([])
            for grid_y in range(self.mapsize):
                map_tile = self.grid_to_map(grid_x, grid_y, r_noise)
                map[grid_x].append(map_tile)




        return map

    def grid_to_map(self, grid_x, grid_y, r_noise):

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        
        #r = random.randint(1, 200)
        r_octave=random.randint(1,9)
        rndnoise = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale, octaves=r_octave) #octaves pour la "naturalité" des forêts
        rndnoisewater = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale)
        
        if (rndnoise >= r_noise):
            tile = "wood"
        elif (rndnoisewater <= -r_noise+10):
            tile = "water"
        elif (rndnoisewater >= -r_noise+10 and rndnoisewater <= -r_noise+10+300*(1/self.mapsize)): #to differentiate world tile from what's on them
            tile = "sand"
        else:
            # if r == 1:
            #    tile = "beeg_wood"
            if rndnoise >= 2 and rndnoise <= 2.3:        #not too much stone
                tile = "stone"
            elif rndnoise <= -2 and rndnoise >= -2.2:       #gold rarer than stone
                tile = "gold"
            elif rndnoise >= 6 and rndnoise <= 6.1:       #single woods kinda rare
                tile = "wood"
            elif (rndnoise <= r_noise-1 and rndnoise >= r_noise-2) or rndnoise >= 6.1 and rndnoise <= 6.6:   #bush près des arbres
                tile = "food"
            else:
                tile = ""

        out = {
            "grid" : [grid_x, grid_y],
            "cart_rect" : rect,
            "iso_poly" : iso_poly,
            "render_pos" : [minx, miny],
            "tile" : tile,
            "collision" : True if tile == "wood" or tile == "gold" or tile == "stone" or tile == "food" else False,
            "water" : True if tile == "water" else False,
            "resources" : 1000 if (tile == "wood" or tile == "food") else (5000 if tile == "gold" or tile == "stone" else 0),
            "whale" : True if (tile == "water" and random.randint(1,10000) == 1) else False,
            "troop": False
        }
        return out

    # def create_collision_matrix(self):
    #     collision_matrix = [[1 for x in range(self.mapsize)] for y in range(self.mapsize)]
    #     for x in range(self.mapsize):
    #         for y in range(self.mapsize):
    #             if self.map[x][y]["collision"]:
    #                 collision_matrix[y][x] = 0
    #     return collision_matrix
    
    # def create_water_matrix(self):
    #     water_matrix = [[1 for x in range(self.mapsize)] for y in range(self.mapsize)]
    #     for x in range(self.mapsize):
    #         for y in range(self.mapsize):
    #             if self.map[x][y]["water"]:
    #                 water_matrix[y][x] = 0
    #     return water_matrix

    def create_mixed_matrix(self):
        # to manage the obstacles : collision and water (used for pathfinding)
        # 1: Empty  0: Occupied
        mixed_matrix = [[1 for x in range(self.mapsize)] for y in range(self.mapsize)]
        for x in range(self.mapsize):
            for y in range(self.mapsize):
                if self.map[x][y]["collision"] or self.map[x][y]["water"]:
                    mixed_matrix[y][x]=0
        return mixed_matrix

    def update_mixed_matrix(self, x, y):
        self.map[x][y]["collision"] = True
        self.mixed_matrix[y][x] = 0

    def create_vision_matrix(self):
        return [[0 for x in range(self.mapsize+10)] for y in range(self.mapsize+10)]

    def update_vision_matrix(self, coords, fov):
        for x in range(-fov+1, fov+1):
            for y in range (-fov+1, fov+1):
                self.vision_matrix[coords[0]+x][coords[1]+y] = 1


    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    



    def can_place_tile(self, grid_pos):
        # check if we can place a tile
        # can place a tile if the mouse is not on a hud or outside the map
        mouse_on_panel = False
        if self.vision_matrix[grid_pos[0]][grid_pos[1]]:
            vision = True
        else : vision = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        map_bounds = (0 <= grid_pos[0] <= self.mapsize) and (0 <= grid_pos[1] <= self.mapsize)

        if map_bounds and not mouse_on_panel and vision:
            return True
        else:
            return False

    def mouse_to_grid_remastered(self,x,y):
        map_x = x - self.grass_tiles_width / 2
        map_y = y
        cart_y = (2* map_y - map_x) / 2
        cart_x = cart_y + map_x
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x +51, grid_y - 50

    def mouse_to_grid(self, x, y, scroll):
        # transform to map position (removing camera scroll and offset)
        map_x = x - scroll.x - self.grass_tiles_width / 2
        map_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * map_y - map_x) / 2
        cart_x = cart_y + map_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def mouse_to_grid_reversed(self,x,y,scroll):
        map_x = x - scroll.x - self.grass_tiles_width / 2
        map_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * map_y - map_x) / 2
        cart_x = cart_y + map_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def load_save(self):
        new_save = save()
        try:
            self.map=new_save.load_Map()
            for grid_x in range(self.mapsize):
                for grid_y in range(self.mapsize):
                    tiletype = self.map[grid_x][grid_y]['tile']
                    render_pos = self.map[grid_x][grid_y]['render_pos']
                    if tiletype =='water':
                        self.grass_tiles.blit(self.tiles["water"],(render_pos[0] + self.grass_tiles_width / 2, render_pos[1]))
                    elif tiletype == "sand":
                        self.grass_tiles.blit(self.tiles["sand"],(render_pos[0] + self.grass_tiles_width / 2, render_pos[1]))

                    else:
                        self.grass_tiles.blit(self.tiles["block"],(render_pos[0] + self.grass_tiles_width / 2, render_pos[1]))
        except FileNotFoundError:
            self.map = self.create_map()
            new_save.save_Map(self.map)

        except EOFError:
            self.map = self.create_map()
        
        new_save = save()
        try:
            self.map=new_save.load_Map()
            for grid_x in range(self.mapsize):
                for grid_y in range(self.mapsize):
                    tiletype = self.map[grid_x][grid_y]['tile']
                    render_pos = self.map[grid_x][grid_y]['render_pos']
                    if tiletype =='water':
                        self.grass_tiles.blit(self.tiles["water"],(render_pos[0] + self.grass_tiles_width / 2, render_pos[1]))
                    elif tiletype == "sand":
                        self.grass_tiles.blit(self.tiles["sand"],(render_pos[0] + self.grass_tiles_width / 2, render_pos[1]))

                    else:
                        self.grass_tiles.blit(self.tiles["block"],(render_pos[0] + self.grass_tiles_width / 2, render_pos[1]))
        except FileNotFoundError:
            self.map = self.create_map()
            new_save.save_Map(self.map)

        except EOFError:
            self.map = self.create_map()
        
        new_save = save()

        buildings = [[None for x in range(self.mapsize)] for y in range(self.mapsize)]

        try:
            self.buildings=new_save.load_buildings()
        except FileNotFoundError:
            new_save.save_buildings(buildings)
            self.buildings = buildings
        except EOFError:
           self.buildings = buildings

        
