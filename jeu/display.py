import pygame as pg
import sys
from .map import Map
from utils.settings import *
from utils.util_functions import draw_text,spawn_enemy_unit,spawn_ally_unit
from .camera import Camera
from .hud import Hud
from .resource_manager import ResourceManager
from entities.units.unit import *
from entities.units.worker import Herobrine

class Display:

    def __init__(self, screen, clock,entities,resource_manager,hud,map,camera):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.cheat = CHEAT
        grid_length_x, grid_length_y = WORLD_SIZE, WORLD_SIZE
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        # entities
        self.entities = entities

        # resource manager
        self.resource_manager = resource_manager

        # hud
        self.hud = hud

        # Map
        self.map = map


        # camera
        self.camera = camera
        self.camera.scroll.x = -int(31.6*WORLD_SIZE - 600)

        self.camera.scroll.y = WORLD_SIZE
        self.whaleimage = pg.image.load("assets/graphics/whale.png").convert_alpha()
        self.fogofwar = pg.image.load("assets/graphics/fogofwar.png").convert_alpha()
        self.fogofwar.set_alpha(1000*FOW_YESORNO)
        self.grass_tiles = pg.Surface(
            (grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()

        self.vision_matrix = map.create_vision_matrix()
        #self.update_vision_matrix = map.create_vision_matrix()
        self.mixed_matrix = map.create_mixed_matrix()

        global x1,y1 # GoodTH position
        x1,y1=WORLD_SIZE/2,WORLD_SIZE/2
        # using mixed_matrix
        # to place TH and have empty tiles around to spawn troops
        # Can be extended if we want more visibility
        while ((WORLD_SIZE-WORLD_SIZE/5 > x1 > WORLD_SIZE/5)
               or (WORLD_SIZE-WORLD_SIZE/5 > y1 > WORLD_SIZE/5)
               # for GoodTH
               or not(self.mixed_matrix[x1][y1] and self.mixed_matrix[x1][y1+1] and
                      self.mixed_matrix[x1-1][y1+1] and self.mixed_matrix[x1+1][y1+1] and self.mixed_matrix[x1][y1-2]
                      # for EnnemyTH
                      and self.mixed_matrix[WORLD_SIZE-x1][WORLD_SIZE-y1] and self.mixed_matrix[WORLD_SIZE-x1][WORLD_SIZE-y1+1] and
                      self.mixed_matrix[WORLD_SIZE-x1-1][WORLD_SIZE-y1+1] and self.mixed_matrix[WORLD_SIZE-x1+1][WORLD_SIZE-y1+1]
                      and self.mixed_matrix[WORLD_SIZE-x1][WORLD_SIZE-y1-2])):

            x1,y1 = random.randint(3,10),random.randint(3,10)

        #GoodTH
        self.goodTH_x = x1
        self.goodTH_y = y1
        render_pos = self.map.map[x1][y1]["render_pos"]
        ent = GoodTH(render_pos, self.resource_manager)
        self.entities.append(ent)
        self.map.buildings[x1][y1] = ent
        self.map.update_mixed_matrix(x1,y1)
        self.map.update_vision_matrix((x1,y1),ent.fieldofview)

        #EnnemyTH
        self.ennemyTH_x = WORLD_SIZE-x1
        self.ennemyTH_y = WORLD_SIZE-y1
        render_pos = self.map.map[WORLD_SIZE-x1][WORLD_SIZE-y1]["render_pos"]
        ent = EnemyTH(render_pos, self.resource_manager)
        self.entities.append(ent)
        self.map.buildings[WORLD_SIZE-x1][WORLD_SIZE-y1] = ent
        self.map.update_mixed_matrix(WORLD_SIZE-x1, WORLD_SIZE-y1)

        self.temp_tile = map.temp_tile
        self.examine_tile = map.examine_tile
        self.examine_troop = map.examine_troop


    def load_images(self):

        # chargement des images
        block = pg.image.load("assets/graphics/block.png").convert_alpha()
        sawmill = pg.image.load("assets/graphics/sawmill.png").convert_alpha()
        mason = pg.image.load("assets/graphics/mason.png").convert_alpha()
        wood = pg.image.load("assets/graphics/tree.png").convert_alpha()
        stone = pg.image.load("assets/graphics/stone.png").convert_alpha()
        birch = pg.image.load("assets/graphics/birch.png").convert_alpha()
        beeg_wood = pg.image.load("assets/graphics/beeg_tree.png").convert_alpha()
        gold = pg.image.load("assets/graphics/gold.png").convert_alpha()
        farm = pg.image.load("assets/graphics/farm.png").convert_alpha()
        townhall = pg.image.load("assets/graphics/townhall.png").convert_alpha()
        enemytownhall = pg.image.load("assets/graphics/enemytownhall.png").convert_alpha()
        water = pg.image.load("assets/graphics/water.png").convert_alpha()
        sand = pg.image.load("assets/graphics/sand.png").convert_alpha()
        Barrack = pg.image.load("assets/graphics/Barrack.png").convert_alpha()
        Archery_range = pg.image.load("assets/graphics/Archery_range.png").convert_alpha()
        Stable = pg.image.load("assets/graphics/Stable.png").convert_alpha()
        Armory = pg.image.load("assets/graphics/armory.png").convert_alpha()
        whale = pg.image.load("assets/graphics/whale.png").convert_alpha()
        food = pg.image.load("assets/graphics/berry_bush.png").convert_alpha()

        images = {
            "sawmill": sawmill,
            "mason": mason,
            "wood": wood,
            "stone": stone,
            "block": block,
            "birch": birch,
            "beeg_wood": beeg_wood,
            "gold": gold,
            "farm": farm,
            "Town Hall": townhall,
            "Enemy Town Hall": enemytownhall,
            "water": water,
            "sand": sand,
            "Barrack": Barrack,
            "Archery range": Archery_range,
            "Stable": Stable,
            "Armory": Armory,
            "whale": whale,
            "food": food
        }

        return images

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.drawMap(self.screen,self.camera)
        #self.map.draw(self.screen, self.camera)
        self.hud.draw(self.screen)

    def drawMap(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.map.map[x][y]["render_pos"]
                # draw map tiles
                tile = self.map.map[x][y]["tile"]

                if not self.map.vision_matrix[x][y]:
                    screen.blit(self.fogofwar,
                                (render_pos[0]-1 + self.map.grass_tiles_width / 2 + camera.scroll.x,
                                 render_pos[1]-1 - (70 - TILE_SIZE) + camera.scroll.y))
                else:

                    if tile != "" and tile != "water" and tile != "sand":
                        screen.blit(self.tiles[tile],
                                    (render_pos[0] + self.map.grass_tiles_width / 2 + camera.scroll.x,
                                     render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    elif tile == "water" and self.map.map[x][y]["whale"]:
                        screen.blit(self.map.whaleimage,
                                    (render_pos[0] + self.map.grass_tiles_width / 2 + camera.scroll.x,
                                     render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    if tile == "water":
                        self.grass_tiles.blit(self.tiles["water"],(render_pos[0] + self.map.grass_tiles_width / 2, render_pos[1]))
                    elif tile == "sand":
                        self.grass_tiles.blit(self.tiles["sand"],(render_pos[0] + self.map.grass_tiles_width / 2, render_pos[1]))
                    else:
                        self.grass_tiles.blit(self.tiles["block"],(render_pos[0] + self.map.grass_tiles_width / 2, render_pos[1]))

                    # draw buildings
                    building = self.map.buildings[x][y]
                    worker = self.map.workers[x][y]

                    if building is not None:
                        worker = None
                        for building_name in dict_buildings:
                            if building.name == building_name:
                                image = pg.image.load(dict_buildings[building_name])
                                if building.in_construction:
                                    image.set_alpha(100)

                                screen.blit(image,
                                            (render_pos[0] + self.map.grass_tiles_width / 2 + camera.scroll.x,
                                             render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))

                                if self.hud.examined_tile is not None:
                                    if (x == self.map.examine_tile[0]) and (y == self.map.examine_tile[1]):
                                        mask = pg.mask.from_surface(image).outline()
                                        mask = [(x + render_pos[0] + self.map.grass_tiles_width / 2 + camera.scroll.x,
                                                 y + render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y)
                                                for x, y in mask]
                                        pg.draw.polygon(screen, (255, 255, 255), mask, 3)

                    # draw workers
                    if worker is not None:
                        building = None
                        for worker_name in dict_workers:
                            if worker.name == worker_name:

                                imageworker = pg.image.load(dict_workers[worker_name])

                                screen.blit(imageworker,
                                            (render_pos[0]+32 + self.map.grass_tiles_width / 2 + camera.scroll.x,
                                             render_pos[1]-16 - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y))


                                if self.hud.examined_troop is not None: # examinating a troop
                                    if (x == self.map.examine_troop.tile["grid"][0]) and (y == self.map.examine_troop.tile["grid"][1]):
                                        image=self.map.examine_troop.image
                                        mask = pg.mask.from_surface(image).outline()
                                        mask = [(x + render_pos[0]+32 + self.map.grass_tiles_width / 2 + camera.scroll.x,
                                                 y + render_pos[1]-16 - (image.get_height() - TILE_SIZE) + camera.scroll.y)
                                                for x, y in mask]
                                        pg.draw.polygon(screen, (40, 165, 250), mask, 2) # to hilight the selected troop


        if self.map.temp_tile is not None:
            # Maintain the spawning place of the troops at "troop" = True
            # Because we don't want to place buildings at these positions
            self.map.map[x1][y1+1]["troop"] = True
            self.map.map[x1-1][y1+1]["troop"] = True
            self.map.map[x1+1][y1+1]["troop"] = True
            self.map.map[x1][y1-2]["troop"] = True

            iso_poly = self.map.temp_tile["iso_poly"]
            iso_poly = [(x + self.map.grass_tiles_width / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in
                        iso_poly]
            if self.map.temp_tile["collision"] or self.map.temp_tile["water"] or self.map.temp_tile["troop"]: # can't place a building here
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3) # red contouring
            elif self.map.placing_building: # can place it
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3) # white contouring
                render_pos = self.map.temp_tile["render_pos"]
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)
                self.map.temp_tile["image"] = img
                screen.blit(
                    self.map.temp_tile["image"],
                    (
                        render_pos[0] + self.map.grass_tiles_width / 2 + camera.scroll.x,
                        render_pos[1] - (self.map.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                    )
                )

        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        mouse_pos = pg.mouse.get_pos()
        grid_pos = self.map.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        if (grid_pos[0] >= 0 and grid_pos[1] >= 0):
            draw_text(screen, str(grid_pos), 30, (255, 255, 255), (mouse_pos[0] + 15, mouse_pos[1] - 15))
        else:
            draw_text(screen, "(X, X)", 30, (255, 255, 255), (mouse_pos[0] + 15, mouse_pos[1] - 15))