import pygame as pg


def draw_text(screen, text, size, color, pos):

    font = pg.font.SysFont(None, size)                    #police par défaut
    text_surface = font.render(text, True, color)         
    text_rect = text_surface.get_rect(topleft=pos)        #get rekt lol

    screen.blit(text_surface, text_rect)
    
    
def spawn_enemy_unit(self,enemy):
    anenemy = enemy(self.map.map[self.map.ennemyTH_x][self.map.ennemyTH_y + 1], self.map)
    self.map.workers.append(anenemy)
    self.map.map[self.map.ennemyTH_x][self.map.ennemyTH_y + 1]["troop"] = True

def spawn_ally_unit(self,ally):
    anally = ally(self.map.map[self.map.goodTH_x][self.map.goodTH_y + 1], self.map)
    self.map.workers.append(anally)
    self.map.map[self.map.goodTH_x][self.map.goodTH_y + 1]["troop"] = True
