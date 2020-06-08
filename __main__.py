# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 17:54:20 2020

@author: ComteHerappait
"""
#%% imports
import pygame
from entity import Entity
from random import uniform
from numpy import floor
from sys import argv
from ScaryBlob import ScaryBlob
from TheJaws import TheJaws
    
def main(number):
    #%% initialization
    pygame.init()
        #variables
    size = width, height = 1800, 900
    
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    black = 0, 0, 0
    white = 255,255,255
    FPS = 60;
    
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
    
    #%% main loop
    running = True
    while running:
        fpsClock.tick(FPS) #limit to 60fps
        time_begin = pygame.time.get_ticks()
        screen.fill(black)

            #movement
        for e in entities:
            e.update(entities, scaryblobs, jaws)
            e.displaySimple(screen)
            
        for sb in scaryblobs:
            sb.display(screen)
        
        for j in jaws:
            j.update(entities, scaryblobs, jaws)
            j.diplayJaws(screen)
            
        #displays text
        textsurface = myfont.render(str(floor(pygame.time.get_ticks()-time_begin))+" ms",
                                    True, (255, 0, 0))
        screen.blit(textsurface,(0,0))
        textsurface = myfont.render("boids : "+str(len(entities))+" blobs : "+str(len(scaryblobs)),
                                    True, (255, 0, 0))
        screen.blit(textsurface,(0,20))
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
               elif event.key == pygame.key.key_code("e"):
                   entities = []
                   scaryblobs = []
                   jaws = []
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

                   
    #%% end
    pygame.quit()
    
    
    
# %% main function
if __name__ == "__main__" :
    if len(argv) == 1:
        number = 20
    else :
        number = int(argv[1])
        
    print("running with :", number, 'entities')
    main(number)