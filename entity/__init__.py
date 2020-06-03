# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:31:52 2020

@author: ComteHerappait
"""
import pygame
from math import atan2, pi, sin, cos, sqrt
from random import uniform, gauss, random
import numpy as np

MAX_SPEED = 3
FRIEND_RADIUS = 120
INDIVIDUAL_SIZE = 20
CONFORT_ZONE = 60

FACTOR_ALIGN   = 10
FACTOR_REJECT  = 100
FACTOR_ATTRACT = 10
FACTOR_NOISE   = 10
FACTOR_DEBUG = False

def addVectors(v1,v2):
    return [v1[0]+v2[0],v1[1]+v2[1]]
    
class Entity:
    """ moving entity for my simulation """
    
    def __init__(self, screensize, speed, screen):
        """constructor"""
        self.screen = screen
        self.speed_ = speed
        self.width_, self.height_ = screensize
        self.center = (self.width_/2, self.height_/2)
        img = pygame.image.load("arrow-white.png")
        self.image_source_ = pygame.transform.scale(img, (INDIVIDUAL_SIZE,INDIVIDUAL_SIZE))
        self.position_ = self.image_source_.get_rect()
        self.position_.move_ip(uniform(0,self.width_), uniform(0,self.height_))
        self.image_ = self.image_source_
        self.friends = []
        
    def update(self, others):                    
        self.warpOnEdges()    
        self.getFriends(others)
                
        self.groupWithFriends()
        self.alignOnFriends()
        self.dodgeFriends()
        self.addNoise(0.05)
        
        self.limitSpeed()
        
        self.move()        
        pygame.draw.circle(self.screen, (0,0,255), self.getPos(), FRIEND_RADIUS, 1)
        #for f in self.friends:
        #    pygame.draw.line(self.screen, (0,255,0), self.getPos(), f.getPos(), 1)
                    
    def move(self):
        self.position_.move_ip(self.speed_)
        angle = -45 + atan2(self.speed_[0],self.speed_[1])*180/pi
            #returns final state of sprite
        self.image_ = pygame.transform.rotate(self.image_source_, angle)
        
    def turn(self, alpha):
        alpha = alpha*180/pi /10000
        x = self.speed_[0]
        y = self.speed_[1]
        self.speed_[0] = cos(alpha)*x - sin(alpha)*y
        self.speed_[1] = sin(alpha)*x + cos(alpha)*y
        
        angle = -45 + atan2(self.speed_[0],self.speed_[1])*180/pi
        self.image_ = pygame.transform.rotate(self.image_source_, angle)
            
    def warpOnEdges(self):
        self.position_[0] = (self.position_[0] + self.width_) % self.width_;
        self.position_[1] = (self.position_[1] + self.height_) % self.height_;
            
    def distance(self, point):
        return sqrt ( (point[0] - self.position_[0])**2 +
                    (  point[1] - self.position_[1])**2  )
    
    def limitSpeed(self, ceiling = MAX_SPEED):
        speedNorm = np.linalg.norm(self.speed_)
        if speedNorm > ceiling :
            self.speed_[0] = self.speed_[0] / (speedNorm/ceiling)
            self.speed_[1] = self.speed_[1] / (speedNorm/ceiling)
                    
    def getFriends(self, others):
        neighbors = [e for e in others if ( 0 < self.distance(e.position_) and self.distance(e.position_) < FRIEND_RADIUS )]
        self.friends = neighbors
    
    def alignOnFriends(self):
        if len(self.friends) == 0 : return
        totalSpeed = (0,0)
        for f in self.friends:
            totalSpeed = addVectors(totalSpeed,f.speed_)
        averageSpeed = [FACTOR_ALIGN * totalSpeed[0]/len(self.friends),
                        FACTOR_ALIGN * totalSpeed[1]/len(self.friends)]
        self.speed_ = addVectors(self.speed_,averageSpeed)
        if FACTOR_DEBUG : print("align : ", np.linalg.norm(averageSpeed))
        
    def addNoise(self, standardDeviation):
        noise = [FACTOR_NOISE * gauss(0,standardDeviation) ,
                 FACTOR_NOISE * gauss(0,standardDeviation) ]
        self.speed_ = addVectors(self.speed_,noise)
        if FACTOR_DEBUG : print("noise : ", np.linalg.norm(noise))
    
    def groupWithFriends(self):
        if len(self.friends) == 0 : return
        friends_pos = [f.getPos() for f in self.friends]
        group_pos = np.average(friends_pos, axis=0)
        vector = [FACTOR_ATTRACT * group_pos[0] - self.position_[0],
                  FACTOR_ATTRACT * group_pos[1] - self.position_[1]]
        self.speed_ = addVectors(self.speed_,vector)
        if FACTOR_DEBUG : print("attract : ", np.linalg.norm(vector))
        
    def dodgeFriends(self):
        if len(self.friends) == 0 : return
        total = [0,0]
        for f in self.friends:
            if (self.distance(f.getPos()) < CONFORT_ZONE):
                pos = f.getPos()
                d = self.distance(pos)
                vect = [self.position_[0]-pos[0], self.position_[1]-pos[1]]
                weighted = [FACTOR_REJECT * vect[0]/d,
                            FACTOR_REJECT * vect[1]/d]
                total = addVectors(total, weighted)
        self.speed_ = addVectors(self.speed_,total)
        if FACTOR_DEBUG : print("reject : ", np.linalg.norm(total))        
        #pygame.draw.circle(self.screen, (255,0,0), self.getPos(), CONFORT_ZONE, 1)
    
    def getPos(self):
        return [ self.position_[0], self.position_[1]]
    
    def reboundOnEdges(self, hardborders=False):
        #change direction when hitting wall
        if self.position_.left < 0 or self.position_.right > self.width_:
            self.speed_[0] = -self.speed_[0]
        if self.position_.top < 0 or self.position_.bottom > self.height_:
            self.speed_[1] = -self.speed_[1]
            
        #prevents objects from exiting the screen
        if hardborders:
            self.position_.left  = max(self.position_.left ,0)
            self.position_.bottom  = max(self.position_.bottom ,0)
            self.position_.right = min(self.position_.right,self.width_)
            self.position_.top = min(self.position_.top,self.height_)
            
    def __del__(self):
        """destructor"""
        pass