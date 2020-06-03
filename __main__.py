# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 17:54:20 2020

@author: ComteHerappait
"""
#%% imports
import pygame
from entity import Entity, FRIEND_RADIUS
from random import uniform
from numpy import floor
from sys import argv

    
    
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
    speeds = [[uniform(-10,10), uniform(-10,10)] for i in range(number)]
    entities = [Entity(size, s, screen) for s in speeds]
    #%% main loop
    running = True
    while running:
        fpsClock.tick(FPS) #limit to 60fps
        
        screen.fill(black)

            #movement
        for e in entities:
            e.update(entities)
            screen.blit(e.image_,e.position_)
            
            
        #displays text
        textsurface = myfont.render(str(floor(fpsClock.get_fps()))+" fps", True, (255, 0, 0))
        screen.blit(textsurface,(0,0))
        
        #finalize display, flips it to the user
        pygame.display.flip()
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   running = False  
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