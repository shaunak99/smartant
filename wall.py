### WALL OBJECT
import pygame

class Wall:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collide(self,ant):
        if ant.x < self.x or ant.x > self.width or ant.y < 0 or ant.y > self.height:
            return 1
        return 0

    def get_coords(self):
        points = []

        for i in range(self.width//10):
            points.append((i*10,self.y))
            points.append((i*10,self.height))
        for i in range(self.height//10):
            points.append((self.x,i*10))
            points.append((self.width,i*10))

        return points

    def draw(self,win):
        x1,y1 = self.x, self.height
        x2,y2 = self.width, self.height
        x3,y3 = self.width, self.y

        pygame.draw.line(win,(255,255,255),(x1,y1),(x2,y2))
        pygame.draw.line(win,(255,255,255),(x3,y3),(x2,y2))
