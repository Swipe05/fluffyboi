from entities.buildings.building import Building


class Sawmill(Building):

    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, map)
        self.name = "Sawmill"
        self.lore = " : Generates Wood over time."
        self.hp = 150
        self.fieldofview = 3
        self.resource_manager.apply_cost_to_resource(self.name)
