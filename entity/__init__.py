# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:31:52 2020

@author: ComteHerappait
"""
from math import sqrt
from random import uniform, gauss

import numpy as np
import pygame

from myVector import myVector

FRIEND_RADIUS = 120
INDIVIDUAL_SIZE = 30
CONFORT_ZONE = 60

BORDER_X = 20
BORDER_Y = 20

FACTOR_ALIGN = 1
FACTOR_REJECT = 1
FACTOR_ATTRACT = 1
FACTOR_DEBUG = False


class Entity:
    """ moving entity for my simulation """

    def __init__(self, screen, pos, speed):
        """constructor"""
        self.alive = True
        self.MAX_SPEED = 7 + gauss(0, 1)
        self.speed_ = myVector(speed[0], speed[1])
        self.width_, self.height_ = screen.get_size()
        self.position_ = pygame.Rect(pos[0], pos[1], 0, 0)
        self.friends = []
        self.color = [uniform(0, 255), uniform(0, 255), uniform(0, 255)]

    def update(self, entities, scaryblobs, jaws):
        self.getFriends(entities)

        _group = self.groupWithFriends()
        _align = self.alignOnFriends()
        _dodge = self.dodgeFriends()
        _scare = self.dodgeScary(scaryblobs)
        _edges = self.dodgeEdges()
        _enemy = self.dodgeJaws(jaws)

        _group.multiply(0.5)
        _enemy.multiply(1)
        _dodge.multiply(2)
        _edges.multiply(2)

        if _group.getNorm() > 0: self.speed_.add(_group)
        if _align.getNorm() > 0: self.speed_.add(_align)
        if _dodge.getNorm() > 0: self.speed_.add(_dodge)
        if _scare.getNorm() > 0: self.speed_.add(_scare)
        if _edges.getNorm() > 0: self.speed_.add(_edges)
        if _enemy.getNorm() > 0: self.speed_.add(_enemy)

        self.addNoise()
        self.limitSpeed(self.MAX_SPEED + len(self.friends) / 10)  # more friends -> faster speed

        self.move()
        self.warpOnEdges()

    def move(self):
        self.position_.move_ip(self.speed_.array())

    def displaySimple(self, screen):
        pos = self.getPos()
        head = [pos[0] - 3 * self.speed_.x, pos[1] - 3 * self.speed_.y]
        pygame.draw.circle(screen, self.camoFriends(), pos, 6)
        pygame.draw.line(screen, self.camoFriends(), pos, head)

    def warpOnEdges(self):
        if (self.position_[0] < BORDER_X):
            self.position_[0] = self.width_ - BORDER_X

        if (self.position_[1] < BORDER_X):
            self.position_[1] = self.height_ - BORDER_Y

        if (self.position_[0] > self.width_ - BORDER_X):
            self.position_[0] = BORDER_X

        if (self.position_[1] > self.height_ - BORDER_X):
            self.position_[1] = BORDER_Y

    def distance(self, point):
        return sqrt((point[0] - self.position_[0]) ** 2 +
                    (point[1] - self.position_[1]) ** 2)

    def limitSpeed(self, ceiling):
        speedNorm = self.speed_.getNorm()
        if speedNorm > ceiling:
            self.speed_.multiply(ceiling / self.speed_.getNorm())

    def getFriends(self, others):
        neighbors = [e for e in others if
                     (0 < self.distance(e.position_) and self.distance(e.position_) < FRIEND_RADIUS)]
        self.friends = neighbors

    def alignOnFriends(self):
        if len(self.friends) == 0: return myVector(0, 0)
        totalSpeed = myVector(0, 0)
        for f in self.friends:
            totalSpeed.add(f.speed_)
        totalSpeed.normalize()
        return totalSpeed

    def addNoise(self):
        if uniform(0, 1) < 0.1:
            angle = gauss(0, 10)
        else:
            angle = 0
        self.speed_.rotate(angle)

    def groupWithFriends(self):
        if len(self.friends) == 0: return myVector(0, 0)
        friends_pos = [f.getPos() for f in self.friends]
        group_pos = np.average(friends_pos, axis=0)
        vector = myVector((group_pos[0] - self.position_[0]),
                          (group_pos[1] - self.position_[1]))
        vector.normalize()
        return vector

    def dodgeFriends(self):
        if len(self.friends) == 0: return myVector(0, 0)
        total = myVector(0, 0)
        for f in self.friends:
            pos = f.getPos()
            d = self.distance(pos)
            if d < CONFORT_ZONE and d > 0:
                vect = myVector(self.position_[0] - pos[0], self.position_[1] - pos[1])
                vect.multiply(1 / d)
                total.add(vect)
        total.normalize()
        return total

    def dodgeScary(self, scaryblobs):
        if len(scaryblobs) == 0: return myVector(0, 0)
        total = myVector(0, 0)
        for sb in scaryblobs:
            dist = self.distance(sb.position)
            if dist < sb.DEATH_ZONE:
                self.color = (255, 255, 255)
                self.die()
            if dist < FRIEND_RADIUS and dist > 0:
                vect = myVector(self.position_[0] - sb.position[0], self.position_[1] - sb.position[1])
                vect.multiply(1 / dist)
                total.add(vect)
        total.normalize()
        return total

    def dodgeEdges(self):
        dodge = myVector(0, 0)
        if self.position_[0] < FRIEND_RADIUS:
            dodge = myVector(self.width_ / 2 - self.position_[0], self.height_ / 2 - self.position_[1])
        elif self.position_[1] < FRIEND_RADIUS:
            dodge = myVector(self.width_ / 2 - self.position_[0], self.height_ / 2 - self.position_[1])
        elif self.position_[0] > self.width_ - FRIEND_RADIUS:
            dodge = myVector(self.width_ / 2 - self.position_[0], self.height_ / 2 - self.position_[1])
        elif self.position_[1] > self.height_ - FRIEND_RADIUS:
            dodge = myVector(self.width_ / 2 - self.position_[0], self.height_ / 2 - self.position_[1])

        dodge.normalize()
        return dodge

    def dodgeJaws(self, jaws):
        if len(jaws) == 0: return myVector(0, 0)
        total = myVector(0, 0)
        for j in jaws:
            dist = self.distance(j.position_)
            if dist < FRIEND_RADIUS and dist > 0:
                vect = myVector(self.position_[0] - j.position_[0], self.position_[1] - j.position_[1])
                vect.multiply(1 / dist)
                total.add(vect)
        total.normalize()
        return total

    def camoFriends(self):
        if len(self.friends) == 0: return self.color
        R = self.color[0]
        G = self.color[1]
        B = self.color[2]
        for f in self.friends:
            R += f.color[0]
            G += f.color[1]
            B += f.color[2]
        return (R / (len(self.friends) + 1),
                G / (len(self.friends) + 1),
                B / (len(self.friends) + 1))

    def getPos(self):
        return [self.position_[0], self.position_[1]]

    def newScreen(self, screen):
        self.width_, self.height_ = screen.get_size()

    def die(self):
        self.alive = False

    def isAlive(self):
        return self.alive
