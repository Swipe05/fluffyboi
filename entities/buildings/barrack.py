from entities.buildings.building import Building


class Barrack(Building):
    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, map)
        self.name = "Barrack"
        self.lore = " : Trains your infantry"
        self.hp = 500
        self.fieldofview = 5
        self.resource_manager.apply_cost_to_resource(self.name)
       
