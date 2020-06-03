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
FRIEND_RADIUS = 100
INDIVIDUAL_SIZE = 10

def addVectors(v1,v2):
    return [v1[0]+v2[0],v1[1]+v2[1]]
    
class Entity:
    """ moving entity for my simulation """
    
    def __init__(self, screensize, speed):
        """constructor"""
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
        
        self.getFriends(others)
        self.warpOnEdges()
        self.groupWithFriends()
        self.alignOnFriends()
        self.dodgeFriends()
        #self.addNoise(0.07)
        
        self.limitSpeed()
        self.move()

                    
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
        averageSpeed = (totalSpeed[0]/len(self.friends),totalSpeed[1]/len(self.friends))
        self.speed_ = addVectors(self.speed_,averageSpeed)
        
    def addNoise(self, standardDeviation):
        self.speed_ = addVectors(self.speed_,[gauss(0,standardDeviation),gauss(0,standardDeviation)])
        
    def groupWithFriends(self):
        if len(self.friends) == 0 : return
        friends_pos = [f.position_[:2] for f in self.friends]
        group_pos = np.average(friends_pos, axis=0)
        vector = [group_pos[0] - self.position_[0], group_pos[1] - self.position_[1]]
        self.speed_ = addVectors(self.speed_,vector)
        
    def dodgeFriends(self):
        if len(self.friends) == 0 : return
        weightedAvoid = [ [self.position_[0]-f.position_[0]/self.distance(f.position_[:2]),
                           self.position_[1]-f.position_[0]/self.distance(f.position_[:2])] 
                        for f in self.friends]
        weightedAvoid = []
        for f in self.friends:
            vector = [self.position_[0]-f.position_[0], self.position_[1]-f.position_[0]] 
            N = np.linalg.norm(vector) 
            vector[0] = vector[0] / N * self.distance(f.position_[:2])
            vector[1] = vector[1] / N * self.distance(f.position_[:2])
            weightedAvoid. append(vector)
        DodgeVector = np.average(weightedAvoid, axis=0)
        self.speed_ = addVectors(self.speed_,DodgeVector)
        
        
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