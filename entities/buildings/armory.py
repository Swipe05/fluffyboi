from entities.buildings.building import Building


class Armory(Building):
    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, map)
        self.name = "Armory"
        self.lore = " : Research and Developpement"
        self.hp = 700
        self.fieldofview = 5
        self.resource_manager.apply_cost_to_resource(self.name)
        