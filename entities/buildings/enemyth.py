from entities.buildings.building import Building


class EnemyTH(Building):

    def __init__(self, pos, resource_manager):
        super().__init__(pos, resource_manager)
        self.team = 2
        self.name = "Enemy Town Hall"
        self.lore = " : The main building of the enemy's city."
        self.hp = 1500
        
    
    def update(self):
        pass