import pygame as pg
from utils.util_functions import draw_text
from utils.button import Button
from entities.units.unit import *
from entities.buildings.building import *
from utils.sprite import dict_buildings

class Hud:

    def __init__(self, resource_manager, width, height):

        self.resource_manager = resource_manager
        self.width = width
        self.height = height

        self.hud_colour = (198, 155, 93, 175)

        # resouces hud
        self.resouces_surface = pg.Surface((width, height * 0.02), pg.SRCALPHA)
        self.resources_rect = self.resouces_surface.get_rect(topleft=(0, 0))
        self.resouces_surface.fill(self.hud_colour)

        # building hud
        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74))
        self.build_surface.fill(self.hud_colour)

        # select hud
        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.select_surface.fill(self.hud_colour)

        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        self.selected_tile = None
        self.examined_tile = None
        self.examined_troop = None

        self.creerworker = False
        self.creerswordman = False
        self.creerbowman = False
        self.creerhorseman = False

    def create_build_hud(self):

        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]
        object_width = self.build_surface.get_width() // 5

        tiles = []

        for image_name, image in self.images.items():

            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect,
                    "affordable": True
                }
            )

            render_pos[0] += image_scale.get_width() + 10

        return tiles

    def update(self):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()


        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if self.resource_manager.is_affordable(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False
            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):

        # resouce hud
        screen.blit(self.resouces_surface, (0, 0))
        # build hud
        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))

        # build select hud
        if self.examined_tile is not None:
            self.examined_troop = None
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            #modif test pour la sauvegarde
            for building_name in dict_buildings:
                if self.examined_tile.name == building_name:
                    image = pg.image.load(dict_buildings[building_name])
                    img = image.copy()
                    img_scale = self.scale_image(img, h=h*0.7)
                    screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 40))
                    draw_text(screen, self.examined_tile.name, 35, (255, 255, 255), self.select_rect.topleft)

                    
            img_scale = self.scale_image(img, h=h*0.7)
            screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 40))
            # draw_text(screen, self.examined_tile.name, 40, (255, 255, 255), self.select_rect.topleft)
            worker_img = pg.image.load('assets/menu/worker_button.png').convert_alpha()
            swordman_img = pg.image.load('assets/menu/swordmanbutton.png').convert_alpha()
            bowman_img = pg.image.load('assets/menu/bowmanbutton.png').convert_alpha()
            horseman_img = pg.image.load('assets/menu/horsemanbutton.png').convert_alpha()


            if isinstance(self.examined_tile,GoodTH):
                bouton_creer_villager = Button(self.width * 0.46, self.height * 0.85,worker_img,0.5)
                if bouton_creer_villager.draw(screen):
                    draw_text(screen, "bouton worker",50,(255,255,255),(50,50))
                    self.creerworker = True
                else : self.creerworker = False
            if isinstance(self.examined_tile,Barrack):
                bouton_swordman = Button(self.width * 0.46, self.height * 0.85,swordman_img,0.5)
                if bouton_swordman.draw(screen):
                    draw_text(screen, "bouton swordman",50,(255,255,255),(50,50))
                    self.creerswordman = True
                else : self.creerswordman = False
            if isinstance(self.examined_tile,Archery_range):
                bouton_bowman = Button(self.width * 0.46, self.height * 0.85,bowman_img,0.5)
                if bouton_bowman.draw(screen):
                    draw_text(screen, "bouton bowman",50,(255,255,255),(50,50))
                    self.creerbowman = True
                else : self.creerbowman = False
            if isinstance(self.examined_tile,Stable):
                bouton_horseman = Button(self.width * 0.46, self.height * 0.85,horseman_img,0.5)
                if bouton_horseman.draw(screen):
                    draw_text(screen, "bouton horseman",50,(255,255,255),(50,50))
                    self.creerhorseman = True
                else : self.creerhorseman = False
                

        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)
            screen.blit(icon, tile["rect"].topleft)

        #select troop hud
        if self.examined_troop is not None: #a patcher
            self.examined_tile = None
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            #modif test pour la sauvegarde
            for worker_name in dict_workers:
                if self.examined_troop.name == worker_name:
                    image = pg.image.load(dict_workers[worker_name])
                    img = image.copy()
                    img_scale = self.scale_image(img, h=h*0.7)
                    screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 40))
                    draw_text(screen, self.examined_troop.name, 35, (255, 255, 255), self.select_rect.topleft)
                    draw_text(screen, (str(self.examined_troop.hp) + "/" + str(self.examined_troop.maxhp) + " HP"), 30, (255, 255, 255), (self.select_rect.centerx + 90, self.select_rect.centery-10))
                    
            img_scale = self.scale_image(img, h=h*0.7)
            screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 40))
            
        # resources
        pos = self.width - 700
        for resource, resource_value in self.resource_manager.resources.items():
            txt = resource + ": " + str(resource_value) + "  "
            draw_text(screen, txt, 30, (255, 255, 255), (pos, 0))
            pos += 160


    def load_images(self):

        # read images
        #sawmill = pg.image.load("assets/graphics/sawmill.png")
        # mason = pg.image.load("assets/graphics/mason.png")
        # farm = pg.image.load("assets/graphics/farm.png")
        # townhall = pg.image.load("assets/graphics/townhall.png").convert_alpha()
        # enemytownhall = pg.image.load("assets/graphics/enemytownhall.png").convert_alpha()
        
        barrack = pg.image.load("assets/graphics/barrack.png").convert_alpha()
        archery_range = pg.image.load("assets/graphics/archery_range.png").convert_alpha()
        stable = pg.image.load("assets/graphics/stable.png").convert_alpha()
        armory = pg.image.load("assets/graphics/armory.png").convert_alpha()

        images = {
            #"Sawmill": sawmill,
            # "Mason": mason,
            # "Farm":farm,
            # "Town Hall": townhall,
            "Barrack": barrack,
            "Archery range": archery_range,
            "Stable": stable,
            "Armory": armory

        }

        return images

    def scale_image(self, image, w=None, h=None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image