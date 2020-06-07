# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:31:52 2020

@author: ComteHerappait
"""
import pygame
from math import atan2, pi, sqrt
from random import uniform, gauss
import numpy as np
from myVector import myVector

MAX_SPEED = 3
FRIEND_RADIUS = 120
INDIVIDUAL_SIZE = 30
CONFORT_ZONE = 60

FACTOR_ALIGN   = 1
FACTOR_REJECT  = 1
FACTOR_ATTRACT = 1
FACTOR_NOISE   = 1
FACTOR_DEBUG = False

def addVectors(v1,v2):
    return [v1[0]+v2[0],v1[1]+v2[1]]
    
class Entity:
    """ moving entity for my simulation """
    
    def __init__(self, screen, pos, speed):
        """constructor"""
        #print("entity : ",screensize, speed, screen)
        self.screen = screen
        self.speed_ = myVector(speed[0],speed[1])
        self.width_, self.height_ = screen.get_size()
        img = pygame.image.load("arrow-white.png")
        self.image_source_ = pygame.transform.scale(img, (INDIVIDUAL_SIZE,INDIVIDUAL_SIZE))
        self.position_ = self.image_source_.get_rect()
        self.position_.move_ip(pos)
        self.image_ = self.image_source_
        self.friends = []
        
    def update(self, others):                    
            
        self.getFriends(others)
                
        _group = self.groupWithFriends()
        _align = self.alignOnFriends()
        _dodge = self.dodgeFriends()
        #_noise = self.addNoise()
        
        self.speed_.add(_group)
        self.speed_.add(_align)
        self.speed_.add(_dodge)
        #self.speed_.add(_noise)
        
        #self.speed_.rotate(gauss(0,1)/50)
        self.limitSpeed()
        
        self.move()
        self.warpOnEdges()        
        #pygame.draw.circle(self.screen, (0,0,255), self.getPos(), FRIEND_RADIUS, 1)
        pygame.draw.circle(self.screen, (0,0,255), self.getPos(), 2)
        for f in self.friends:
            pygame.draw.line(self.screen, (0,255,0), self.getPos(), f.getPos(), 1)
                    
    def move(self):
        self.position_.move_ip(self.speed_.array())
        
            #returns final state of sprite
        self.image_ = pygame.transform.rotate(self.image_source_, self.speed_.getAngle()+45) #angle offset because of the image used
        
            
    def warpOnEdges(self):
        BORDER_X = 100
        BORDER_Y = 100
        if (self.position_[0] < BORDER_X) :
            self.position_[0] = self.width_ - BORDER_X
            
        if (self.position_[1] < BORDER_X) :
            self.position_[1] = self.height_ - BORDER_Y
            
        if (self.position_[0] > self.width_ - BORDER_X) :
            self.position_[0] = BORDER_X
            
        if (self.position_[1] > self.height_ - BORDER_X) :
            self.position_[1] = BORDER_Y
                        
    def distance(self, point):
        return sqrt ( (point[0] - self.position_[0])**2 +
                    (  point[1] - self.position_[1])**2  )
    
    def limitSpeed(self, ceiling = MAX_SPEED):
        speedNorm = self.speed_.getNorm()
        if speedNorm > ceiling :
            self.speed_.multiply(ceiling/self.speed_.getNorm())
                    
    def getFriends(self, others):
        neighbors = [e for e in others if ( 0 < self.distance(e.position_) and self.distance(e.position_) < FRIEND_RADIUS )]
        self.friends = neighbors
    
    def alignOnFriends(self):
        if len(self.friends) == 0 : return myVector(0,0)
        totalSpeed = myVector(0,0)
        for f in self.friends:
            totalSpeed.add(f.speed_)
        totalSpeed.normalize()
        return totalSpeed
        
    def addNoise(self):
        if (uniform(0,10) > 7) :
            noise = myVector( gauss(0,1) ,
                              gauss(0,1) )
            noise.normalize()
            return noise
        else:
            return myVector(0,0)
    
    def groupWithFriends(self):
        if len(self.friends) == 0 : return myVector(0,0)
        friends_pos = [f.getPos() for f in self.friends]
        group_pos = np.average(friends_pos, axis=0)
        vector = myVector( (group_pos[0] - self.position_[0]) ,
                           (group_pos[1] - self.position_[1]) )
        vector.normalize()
        return vector
        
    def dodgeFriends(self):
        if len(self.friends) == 0 : return myVector(0,0)
        total = myVector(0,0)
        for f in self.friends:
            if (self.distance(f.getPos()) < CONFORT_ZONE):
                pos = f.getPos()
                d = self.distance(pos)
                vect = myVector ( self.position_[0]-pos[0], self.position_[1]-pos[1] )
                vect.multiply(1/d)
                total.add(vect)
        total.normalize()
        return total  
        #pygame.draw.circle(self.screen, (255,0,0), self.getPos(), CONFORT_ZONE, 1)
    
    def getPos(self):
        return [ self.position_[0], self.position_[1]]
                
    def __del__(self):
        """destructor"""
        pass