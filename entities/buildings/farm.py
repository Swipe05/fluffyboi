from entities.buildings.building import Building


class Farm(Building) :

    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, map)
        self.name = "Farm"
        self.lore = " : Generates Food over time."
        self.hp = 350
        self.fieldofview = 3
        self.resource_manager.apply_cost_to_resource(self.name)
