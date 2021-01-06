import pygame
import neat
import os
import random
import time
from ant import Ant
from wall import Wall
from obstacle import Obstacle
from flag import Flag
pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 800

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.jpg")),(WIN_WIDTH,WIN_HEIGHT))

STAT_FONT = pygame.font.SysFont("comicsans",50)

def draw_window(win, ants, obs, flags, wall, alive, madeit):
    win.blit(BG_IMG, (0,0))
    wall.draw(win)

    # flags.draw(win)
    for flag in flags:
        flag.draw(win)

    for o in obs:
        o.draw(win)

    # ants.draw(win)
    for ant in ants:
        ant.draw(win)

    text = STAT_FONT.render("Alive: "+str(alive),1,(255,255,255))
    win.blit(text,(10,10))

    text = STAT_FONT.render("Made It: "+str(madeit),1,(255,255,255))
    win.blit(text,(10,70))

    pygame.display.update()

## Use this main to control with arrow keys
## Remember to comment the second main function if using this
# def main():
#
#     ant = Ant(500,10,40)
#     wall = Wall(0,0,WIN_WIDTH-100,WIN_HEIGHT-100)
#     obs = []
#     for i in range(5):
#         o = (Obstacle(random.randrange(0,WIN_WIDTH-100,1),random.randrange(0,WIN_HEIGHT-100,1)))
#         obs.append(o)
#     win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
#     flag = Flag(700,700)
#     clock = pygame.time.Clock()
#     run = True
#
#     while run:
#         clock.tick(2)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#                 quit()
#
#             if event.type == pygame.KEYDOWN:
#                 ant.move_key(event.key)
#
#         ant.getSensorData(wall,obs,flag)
#         for ob in obs:
#             if ob.collide(ant):
#                 print("Arghhhh")
#
#         draw_window(win,ant,obs,flag,wall,1,0)
#
# main()

obs = []
#Map 1
for i in range(15):
    o = (Obstacle(random.randrange(150,WIN_WIDTH-150,30),random.randrange(150,WIN_HEIGHT-150,30)))
    obs.append(o)

#Map 2
# for i in range(5):
#     o = Obstacle(70*(i+1),250)
#     obs.append(o)
# for i in range(2):
#     o = Obstacle(70*4,250-60*(i+1))
#     obs.append(o)
# for i in range(5):
#     o = Obstacle(70*(5+i),250-50*3)
#     obs.append(o)
# obs.append(Obstacle(700,260))

def main(genomes,config):
    global obs
    nets = []
    ge = []
    ants = []
    flags = []

    idtick = 0
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        ants.append(Ant(100,100,random.randrange(-90,90,20),idtick))
        g.fitness = 0
        ge.append(g)
        flags.append(Flag(650,700,idtick))
        idtick += 1

    # flag = Flag(650,700)
    wall = Wall(0,0,WIN_WIDTH-10,WIN_HEIGHT-10)

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    madeit = 0
    start = time.time()

    while run:
        clock.tick(100)
        nets_c = []
        ge_c = []
        ants_c = []
        flags_c = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        if len(ants) > 0:
            pass
        else:
            run =  False
            break

        for x,ant in enumerate(ants):
            input = ant.getSensorData(wall,obs,flags[x])
            ant.command = nets[x].activate(tuple(input))

            if ant.move():
                ge[x].fitness += 0.1

            if ant.goal(flags[x]):
                ge[x].fitness += 0.5
            else:
                ge[x].fitness -= 0.1

        for x,ant in enumerate(ants):

            if flags[x].reached(ant):
                ge[x].fitness += 100
                madeit += 1
                print("YEA")
                ant.success = 1
                flags[x].x = 100
                flags[x].y = 100

            if ant.stag > 30:
                ge[x].fitness -= 100
                ant.collide = 1

            if wall.collide(ant):
                ge[x].fitness -= 100
                ant.collide = 1

            for ob in obs:
                if ob.collide(ant):
                    ge[x].fitness -= 100
                    ant.collide = 1
                    break

            ### Don't remember if this is still relevant
            # if ant.success == 1:
            #     ants_c = [ants[x]]
            #     ge_c = [ge[x]]
            #     nets_c = [nets[x]]
            #     flags
            #     ant.success = 0
            #     break

            if ant.collide == 0:
                ants_c.append(ants[x])
                ge_c.append(ge[x])
                nets_c.append(nets[x])
                flags_c.append(flags[x])

        ants = ants_c
        ge = ge_c
        nets = nets_c
        flags = flags_c

        alive = len(ants)
        draw_window(win,ants,obs,flags,wall,alive,madeit)
        if time.time()-start > 150:
            print("Too long")
            break

def run(config_path):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    checkpoints = [f for f in os.listdir('.') if os.path.isfile(f)]

    k = 0
    for f in checkpoints:
        if f.find('neat-checkpoint-') != -1:
            k = max(int(k),int(f[-1]))
            #print(k)

    if k:
        name = 'neat-checkpoint-'+str(k)
        print(name)
        p = neat.Checkpointer.restore_checkpoint(name)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        # p.add_reporter(neat.Checkpointer(6))

    p = neat.Checkpointer.restore_checkpoint('first_success')
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,200)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
