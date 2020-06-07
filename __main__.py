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
    
    
def main(number):
    #%% initialization
    pygame.init()
        #variables
    size = width, height = 1024, int(1024)
    
    black = 0, 0, 0
    white = 255,255,255
    FPS = 60;
    
    myfont = pygame.font.SysFont('Arial', 14)
    
    screen = pygame.display.set_mode(size)
    fpsClock = pygame.time.Clock()
    #creates the entities
    speeds = [[uniform(-10,10), uniform(-10,10)]            for i in range(number)]
    positions = [[uniform(0,width), uniform(0,height)]      for i in range(number)]
    entities = [Entity(screen, positions[i], speeds[i] )    for i in range(number)]
    
    #scaryblobs
    scaryblobs = []
    #%% main loop
    running = True
    while running:
        fpsClock.tick(FPS) #limit to 60fps
        time_begin = pygame.time.get_ticks()
        screen.fill(black)

            #movement
        for e in entities:
            e.update(entities, scaryblobs)
            e.displaySimple(screen)
            
        for sb in scaryblobs:
            sb.display(screen)
            
        #displays text
        textsurface = myfont.render(str(floor(pygame.time.get_ticks()-time_begin))+" ms", True, (255, 0, 0))
        screen.blit(textsurface,(0,0))
        
        #finalize display, flips it to the user
        pygame.display.flip()
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               print("closing...(x)")
               running = False
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   print("closing... (esc)")
                   running = False           
           if event.type == pygame.MOUSEBUTTONDOWN:
               pos_down = pygame.mouse.get_pos()
           if event.type == pygame.MOUSEBUTTONUP and pos_down != (0,0):
               pos_up = pygame.mouse.get_pos()
               if event.button == 1: #left click
                   speed = [pos_up[0]-pos_down[0],pos_up[1]-pos_down[1]]
                   entities.append( Entity(screen, pos_down, speed) )
               if event.button == 3: #right click
                   scaryblobs.append(ScaryBlob(pos_up))
                   
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