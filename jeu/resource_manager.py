import pygame as pg
from utils.save import *



class ResourceManager:


    def __init__(self):

        # ally_resources
        new_save = save()
        resources = {
            "wood": 100000,
            "stone": 100000,
            "food": 100000,
            "gold": 50000
        }
        try:
            self.resources = new_save.load_resources()
        except FileNotFoundError:
            new_save.save_resources(resources)
            self.resources = resources
        except EOFError:
            self.resources = resources

        enemy_resources = {
            "wood": 100000,
            "stone": 100000,
            "food": 100000,
            "gold": 2
        }


        #costs
        self.costs = {
            "Sawmill": {"wood": 300, "stone": 300},
            "Mason": {"wood": 300, "stone": 500},
            "Farm": {"wood": 500, "stone": 500},
            "Barrack": {"wood": 500, "stone": 300, "gold": 400},
            "Archery range": {"wood": 200, "stone": 900, "gold": 400},
            "Stable": {"wood": 500, "stone": 500, "gold": 900},
            "Armory": {"wood": 1000, "stone": 1000},
            "Town Hall": {"wood": 0, "stone": 0},
            "Enemy Town Hall": {"wood": 0, "stone": 0}
        }

    def apply_cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable

    def EN_apply_cost_to_resource(self, building):
        for enemy_resource, cost in self.costs[building].items():
            self.enemy_resources[enemy_resource] -= cost

    def EN_is_affordable(self, building):
        affordable = True
        for enemy_resource, cost in self.costs[building].items():
            if cost > self.enemy_resources[enemy_resource]:
                affordable = False
        return affordable


