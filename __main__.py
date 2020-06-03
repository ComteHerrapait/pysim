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
from multiprocessing import Process
from threading import Thread

entities = []
def loop(single, everyone = entities):
    single.update(everyone)
    

def main(number):
    #%% initialization
    pygame.init()
        #variables
    size = width, height = 1024, int(1024)
    
    black = 0, 0, 0
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
        processes = []
        for e in entities:
            #loop(e)
            p = Process(target=loop, args=(e,))
            processes.append(p)
            p.start()
            
        for p in processes:
            p.join()
            
        for e in entities:
            screen.blit(e.image_,e.position_)
            for f in e.friends:
                pygame.draw.line(screen, (0,255,0), e.getPos(), f.getPos(), 1)
            
        #displays text
        textsurface = myfont.render(str(floor(fpsClock.get_fps()))+" fps", True, (255, 0, 0))
        screen.blit(textsurface,(0,0))
        print(floor(fpsClock.get_fps()))
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
    #%% end
    pygame.quit()
    
    
    
# %% main function
if __name__ == "__main__" :
    if len(argv) == 1:
        number = 100
    else :
        number = int(argv[1])
        
    print("running with :", number, 'entities')
    main(number)