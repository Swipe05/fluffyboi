from entities.buildings.building import Building


class GoodTH(Building):

    def __init__(self, pos, resource_manager):
        super().__init__(pos, resource_manager)
        self.name = "Town Hall"
        self.lore = " : The main building of your new city."
        self.hp = 500
        self.fieldofview = 10


    def update(self):
        pass