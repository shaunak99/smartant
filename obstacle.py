###OBSTACLE OBJECT
import pygame
import os

WIDTH = 60
OBSTACLE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","obstacle.png")), (WIDTH,WIDTH))
class Obstacle:
    IMG = OBSTACLE_IMG

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = self.IMG

    def collide(self,ant):
        obst_mask = pygame.mask.from_surface(self.img)
        ant_mask = ant.get_mask()

        offset = (self.x - round(ant.x), self.y - round(ant.y))

        overlap = ant_mask.overlap(obst_mask,offset)

        if overlap:
            return True

        return False

    def get_boundpoints(self):
        # rect = self.img.get_rect(topleft=(self.x,self.y))
        # bounds = [rect.topleft,rect.midtop,rect.topright,rect.midleft,rect.midright,rect.bottomleft,rect.midbottom,rect.bottomright]
        # return bounds

        bounds = []
        for i in range(WIDTH//10):
            bounds.append((self.x,self.y+i*10))
            bounds.append((self.x+WIDTH,self.y+i*10))
            bounds.append((self.x+i*10,self.y))
            bounds.append((self.x+i*10,self.y+WIDTH))
        return bounds

    def draw(self,win):
        pygame.draw.rect(win,(255,0,0),pygame.Rect(self.x,self.y,WIDTH,WIDTH),2)
        win.blit(self.img, (self.x,self.y))
