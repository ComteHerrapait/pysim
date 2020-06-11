#
from entity import Entity
from entity import *
import pygame
#from math import sqrt
from random import uniform, gauss
#import numpy as np
from myVector import myVector
class TheJaws(Entity):
    
    def __init__(self, screen, pos, speed):
        super().__init__(screen, pos, speed)
        self.MAX_SPEED = 7
        self.FOOD_COUNT = 0
        self.EAT_RADIUS = 50
        self.VISION_RADIUS = 180
        
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
        _food  = self.seekFood(entities)
        
        _group.multiply(0.1)
        
        if _group.getNorm() > 0 :self.speed_.add(_group)
        if _align.getNorm() > 0 :self.speed_.add(_align)
        if _dodge.getNorm() > 0 :self.speed_.add(_dodge)
        if _scare.getNorm() > 0 :self.speed_.add(_scare)       
        if _edges.getNorm() > 0 :self.speed_.add(_edges)
        if _food.getNorm() > 0 : self.speed_.add(_food)
        
        self.addNoise()
        self.limitSpeed()
        
        self.move()
        self.warpOnEdges()

    def seekFood(self, food):
        total = myVector(0,0)
        if len(food) == 0 : return total      
        for f in food:
            pos = f.getPos()
            d = self.distance(pos)
            if d < self.EAT_RADIUS:
                f.die()
                self.FOOD_COUNT += 1
            if d < self.VISION_RADIUS and d > 0:              
                vect = myVector ( pos[0] - self.position_[0], pos[1] - self.position_[1] )
                vect.multiply(1/d)
                total.add(vect)
        total.normalize()
        return total  