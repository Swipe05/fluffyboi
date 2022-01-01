from entities.buildings.building import Building


class Mason(Building):

    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, map)
        self.name = "Mason"
        self.lore = " : Generates Stone over time."
        self.hp = 350
        self.fieldofview = 3
        self.resource_manager.apply_cost_to_resource(self.name)
 
