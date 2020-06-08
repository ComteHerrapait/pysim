#
from entity import Entity
from entity import *
import pygame
#from math import sqrt
from random import uniform, gauss
#import numpy as np
#from myVector import myVector

class TheJaws(Entity):
    
    def diplayJaws(self, screen):
        pos = self.getPos()
        head = [pos[0] + 3 * self.speed_.x, pos[1] + 3 * self.speed_.y]
        pygame.draw.circle(screen, (255,0,0), pos, 12)
        pygame.draw.line(screen, (255,255,0), pos, head)

    def update(self, entities, scaryblobs, jaws):
        self.getFriends(jaws)
                
        _group = self.groupWithFriends()
        _align = self.alignOnFriends()
        _dodge = self.dodgeFriends()
        _scare = self.dodgeScary(scaryblobs)
        _edges = self.dodgeEdges()
        
        _group.multiply(0.1)
        
        self.speed_.add(_group)
        self.speed_.add(_align)
        self.speed_.add(_dodge)
        self.speed_.add(_scare)       
        self.speed_.add(_edges)
        
        self.speed_.rotate(gauss(0,1)/50)
        self.limitSpeed()
        
        self.move()
        self.warpOnEdges()
