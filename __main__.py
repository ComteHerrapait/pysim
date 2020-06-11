# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 17:54:20 2020

@author: ComteHerappait
"""
#%% imports
import pygame
from entity import Entity
from random import uniform
from numpy import floor, average, floor
from sys import argv
from ScaryBlob import ScaryBlob
from TheJaws import TheJaws
import matplotlib.pyplot as plt

avgMaxSpeed = []
times = []
numberAlive = []

def plotData(x, y1, y2, plot):
    # plt.plot(times,avgMaxSpeed,numberAlive)                  
    # plt.show()
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('time (ms)')
    ax1.set_ylabel('average speed', color=color)
    ax1.plot(x , y1, color=color)
    ax1.plot([0,x[-1]], [7,7], color='tab:purple')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:blue'
    ax2.set_ylabel('number alive', color=color)  # we already handled the x-label with ax1
    ax2.plot(x , y2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    if plot:
        plt.show()
    else:
        plt.draw()


def main(number):
    #%% initialization
    pygame.init()
        #variables
    size = width, height = 1920, 1020

    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    black = 0, 0, 0
    white = 255, 255, 255
    FPS = 60

    myfont = pygame.font.SysFont('Arial', 14)

    fpsClock = pygame.time.Clock()
    #creates the entities
    speeds = [[uniform(-10,10), uniform(-10,10)]            for i in range(number)]
    positions = [[uniform(0,width), uniform(0,height)]      for i in range(number)]
    entities = [Entity(screen, positions[i], speeds[i] )    for i in range(number)]

    #scaryblobs
    scaryblobs = []

    #The Jaws
    jaws = []

    #average MAX_SPEED of entities
    avgMaxSpeed = [average([e.MAX_SPEED for e in entities])]
    numberAlive = [len(entities)]
    times = [pygame.time.get_ticks()]

    
    #%% main loop
    running = True
    while running:
        fpsClock.tick(FPS) #limit to 60fps
        time_begin = pygame.time.get_ticks()
        screen.fill(black)

        pygame.draw.line(screen, (0,255,0), (20,20), (width-20,20))
        pygame.draw.line(screen, (0,255,0), (width-20,20), (width-20,height-20))
        pygame.draw.line(screen, (0,255,0), (width-20,height-20), (20,height-20))
        pygame.draw.line(screen, (0,255,0), (20,height-20), (20,20))
            #movement
        for j in jaws:
            if j.isAlive() :
                j.update(entities, scaryblobs, jaws)
                j.diplayJaws(screen)
                textsurface = myfont.render(str(floor(j.hunger))[:-2],True, (255, 0, 0))
                screen.blit(textsurface,(j.position_[0]+10,j.position_[1]+10))
            else:
                jaws.remove(j)

        for e in entities:
            if not e.isAlive():
                entities.remove(e)
            else :
                e.update(entities, scaryblobs, jaws)
                e.displaySimple(screen)

        for sb in scaryblobs:
            sb.display(screen)
            
            #kill dead units
        if len(entities) < number and uniform(0, 1) < 0.05:
            entities.append(Entity(screen,
                                   [uniform(0,width), uniform(0,height)],
                                   [uniform(-10,10), uniform(-10,10)]))
            
        #calculates new average max speed
        avgMaxSpeed.append( average([e.MAX_SPEED for e in entities]) )
        times.append(pygame.time.get_ticks())
        numberAlive.append(len(entities))
        
        #displays text
        textsurface = myfont.render(str(floor(pygame.time.get_ticks()-time_begin))+" ms",
                                    True, (255, 0, 0))
        screen.blit(textsurface,(25,25))
        textsurface = myfont.render(str(len(entities))+ "/" + str(number) +"boids   "
                                    +str(len(scaryblobs))+"blobs   "
                                    +str(len(jaws)) + "jaws",
                                    True, (255, 0, 0))
        screen.blit(textsurface,(25,45))
        #finalize display, flips it to the user
        pygame.display.flip()
        for event in pygame.event.get():
            # if event.type == pygame.VIDEORESIZE:
            #     size = width, height = event.dict['size']
            #     screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            #     for e in entities:
            #         e.newScreen(screen)
            # elif  event.type == pygame.VIDEOEXPOSE :
            #     size = width, height = event.dict['size']
            #     screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            #     for e in entities:
            #         e.newScreen(screen)
            if event.type == pygame.QUIT:
               print("closing...(x)")
               running = False
            elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   print("closing... (esc)")
                   running = False
               elif event.key == pygame.K_e:
                   entities = []
                   scaryblobs = []
                   jaws = []
               elif event.key == pygame.K_p:
                   plotData(times, avgMaxSpeed, numberAlive, True)
               elif event.key == pygame.K_o:
                   plotData(times, avgMaxSpeed, numberAlive, False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_down = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and pos_down != (0,0):
                pos_up = pygame.mouse.get_pos()
                if event.button == 1: #left click
                   speed = [pos_up[0]-pos_down[0],pos_up[1]-pos_down[1]]
                   entities.append( Entity(screen, pos_down, speed) )
                elif event.button == 3: #right click
                   scaryblobs.append(ScaryBlob(pos_up))
                elif event.button == 2: #middle click
                   speed = [pos_up[0]-pos_down[0],pos_up[1]-pos_down[1]]
                   jaws.append( TheJaws(screen, pos_down, speed) )
            elif event.type == pygame.MOUSEWHEEL:
                number = max(0,event.y+number)

    #%% end
    pygame.quit()
    
    



# %% main function
if __name__ == "__main__" :
    if len(argv) == 1:
        number = 50
    else :
        number = int(argv[1])

    main(number)
