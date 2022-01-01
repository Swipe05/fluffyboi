from entities.buildings.building import Building


class Archery_range(Building):
    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, map)
        self.name = "Archery range"
        self.lore = " : Trains your bowmen"
        self.hp = 500
        self.fieldofview = 5
        self.resource_manager.apply_cost_to_resource(self.name)
