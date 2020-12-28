###FLAG OBJECT
import pygame
import os

FLAG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","flag.png")), (40,40))

class Flag:
    IMG = FLAG_IMG

    def __init__(self,x,y,id=0):
        self.x = x
        self.y = y
        self.id = id
        self.img = self.IMG

    def draw(self,win):
        win.blit(self.img, (self.x,self.y))

    def reached(self,ant):
        if self.id == ant.id:
            flag_mask = pygame.mask.from_surface(self.img)
            ant_mask = ant.get_mask()

            offset = (self.x - round(ant.x), self.y - round(ant.y))

            overlap = ant_mask.overlap(flag_mask,offset)

            if overlap:
                return True
        return False
