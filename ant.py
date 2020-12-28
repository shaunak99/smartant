### ANT OBJECT
import math
import pygame
import os
import numpy as np
import time

ANT_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","ant.png")), (40,40))

class Ant:
    IMG = ANT_IMG
    ROT_VEL = 25

    def __init__(self,x,y,rot,id=0):
        self.x = x
        self.y = y
        self.rot = rot
        self.id = id
        self.vel = -5
        self.sensor_points = []
        self.command = [0,0,0]
        self.collide = 0
        self.past = 100000
        self.stag = 0
        self.success = 0
        self.img = self.IMG

    def displace(self):
        self.x = self.x + self.vel*math.sin(math.radians(self.rot))
        self.y = self.y + self.vel*math.cos(math.radians(self.rot))

    def backwards(self):
        self.x = self.x - self.vel*math.sin(math.radians(self.rot))
        self.y = self.y - self.vel*math.cos(math.radians(self.rot))

    def rotate_right(self):
        self.rot -= self.ROT_VEL
        if self.rot < 0:
            self.rot = 360 + self.rot

    def rotate_left(self):
        self.rot += self.ROT_VEL
        if self.rot > 0:
            self.rot = self.rot - 360

    def move(self):
        pos = np.argmax(self.command)
        if self.command[pos] > 0.5:
            if pos == 0:
                self.displace()
                self.stag = 0
                return 1
            elif pos == 1:
                self.rotate_right()
                self.stag += 1
                return 0
            elif pos == 2:
                self.rotate_left()
                self.stag += 1
                return 0
        self.stag += 1
        return 0
        # elif pos == 3:
        #     self.backwards()

    def get_ant_rect(self):
        rotated_image = pygame.transform.rotate(self.img, self.rot)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        return rotated_image, new_rect

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def calc_dist(self,x,y,default_dist):
        norm_dist = []
        for p,q in self.sensor_points:
            norm_dist.append(1-(math.hypot(p-x,q-y)/default_dist))

        return norm_dist

    def get_angle(self,a,b,c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        ba = a-b
        bc = c-b

        cosine_angle = np.dot(ba,bc)/(np.linalg.norm(ba)*np.linalg.norm(bc))
        return np.degrees(np.arccos(cosine_angle))

    def get_lineval(self,x,y,a,b,px,py):
        val = (y-b)*(px-a) - (py-b)*(x-a)
        if val < 0:
            return -1
        else:
            return 1

    def getSensorData(self,wall,obs,flag):
        """
        Find extreme coordinates of sensors and take cosine distances.
        +ve means keep 50
        -ve means take the distance from extreme sensor point.
        """

        default_dist = 60
        sensor_data = [1.0,0]
        self.sensor_points = []
        theta = 45

        _, rect = self.get_ant_rect()
        (a,b) = rect.center
        px = a - math.sin(math.radians(self.rot))*default_dist
        py = b - math.cos(math.radians(self.rot))*default_dist

        #Just for line drawing
        for i in [-1,0,1]:
            angle = self.rot - i*theta
            x = a - math.sin(math.radians(angle))*default_dist
            y = b - math.cos(math.radians(angle))*default_dist
            self.sensor_points.append((x,y))

        fl = 0
        count = 0
        for ob in obs:
            corners = ob.get_boundpoints()
            for (x,y) in corners:
                dist = math.hypot(a-x,b-y)
                subt_ang = self.get_angle([x,y],[a,b],[px,py])
                if dist < default_dist and subt_ang < theta:
                    if (dist/default_dist) < sensor_data[0]:
                        sensor_data[0] = min(sensor_data[0],dist/default_dist)
                        sensor_data[1] = subt_ang*self.get_lineval(x,y,a,b,px,py)/theta
                    # print("DIST:",sensor_data[0])
                    # print("ANGLE:",sensor_data[1])
                    fl = 1
                    count += 1
                    if count > 5:
                        break
            if fl:
                break

        count = 0
        b_points = wall.get_coords()
        for (x,y) in b_points:
            dist = math.hypot(a-x,b-y)
            subt_ang = self.get_angle([x,y],[a,b],[px,py])
            if dist < default_dist and subt_ang < theta:
                if (dist/default_dist) < sensor_data[0]:
                    sensor_data[0] = min(sensor_data[0],dist/default_dist)
                    sensor_data[1] = (subt_ang*self.get_lineval(x,y,a,b,px,py))/theta
                # print("DIST:",sensor_data[0])
                # print("ANGLE:",sensor_data[1])
                count += 1
                if count > 5:
                    break

        f_ang = math.sin(math.radians(self.get_angle([flag.x,flag.y],[a,b],[px,py])*self.get_lineval(flag.x,flag.y,a,b,px,py)))
        # print(f_ang)
        sensor_data.append(f_ang)
#        #Old implementation (3 sensors)
#         for i in [-1,0,1]:
#             angle = self.rot - i*theta
#             x = a - math.sin(math.radians(angle))*default_dist
#             y = b - math.cos(math.radians(angle))*default_dist
#             self.sensor_points.append((x,y))
#
#         c_wallx = min(abs(a-wall.x),abs(a-wall.width))
#         c_wally = min(abs(b-wall.y),abs(b-wall.height))
#
# #        print(c_wallx,c_wally,math.hypot(c_wallx,c_wally))
#         if c_wallx < default_dist or c_wally < default_dist:
#             if c_wallx < default_dist:
#                 if c_wallx == abs(a - wall.x):
#                     wx,wy = (a-c_wallx,b)
#                 else:
#                     wx,wy = (a+c_wallx,b)
#             elif c_wally < default_dist:
#                 if c_wally == abs(b - wall.y):
#                     wx,wy =(a,b-c_wally)
#                 else:
#                     wx,wy =(a,b+c_wally)
#
#             dist = math.hypot(a-wx,b-wy)
#             subt_ang = self.get_angle([wx,wy],[a,b],self.sensor_points[1])
#             if dist < default_dist and subt_ang < theta:
#                 sensor_data = self.calc_dist(x,y,default_dist)
#                 # print(sensor_data)
#                 # print(subt_ang)
#
#         flag = 0
#         for ob in obs:
#             corners = ob.get_boundpoints()
#             for (x,y) in corners:
#                 dist = math.hypot(a-x,b-y)
#                 subt_ang = self.get_angle([x,y],[a,b],self.sensor_points[1])
#                 if dist < default_dist and subt_ang < theta:
#                     sensor_data = self.calc_dist(x,y,default_dist)
#                     # print(sensor_data)
#                     # print(subt_ang)
#                     flag = 1
#                     break
#             if flag:
#                 break

        return sensor_data

    def goal(self,flag):
        x,y = flag.x,flag.y
        goal_dist = math.hypot(self.sensor_points[1][0]-x,self.sensor_points[1][1]-y)
        if self.past > goal_dist:
            self.past = goal_dist
            return 1

        return 0

    def move_key(self,key):
        if key == pygame.K_LEFT:
            self.rotate_left()
        if key == pygame.K_RIGHT:
            self.rotate_right()
        if key == pygame.K_UP:
            self.displace()
        if key == pygame.K_DOWN:
            self.backwards()

    def draw(self,win):

        rotated_image, new_rect = self.get_ant_rect()
        win.blit(rotated_image, new_rect.topleft)

        pygame.draw.rect(win,(255,0,0),new_rect,2)
        for (x,y) in self.sensor_points:
            pygame.draw.line(win,(255,255,0),new_rect.center,(x,y))
