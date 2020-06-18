#
# from math import sqrt
from random import gauss

import pygame

from entity import *
from myVector import myVector

EATING_TRIGGER = 10
EATING_AMOUNT = 25


class TheJaws(Entity):

    def __init__(self, screen, pos, speed):
        super().__init__(screen, pos, speed)
        self.MAX_SPEED = 5
        self.EAT_RADIUS = 50
        self.VISION_RADIUS = 180
        self.hunger = 0
        self.posLastEaten = (0, 0)

    def diplayJaws(self, screen):
        pos = self.getPos()
        head = [pos[0] + 3 * self.speed_.x, pos[1] + 3 * self.speed_.y]
        pygame.draw.circle(screen, (255, 0, 0), pos, 15 * (1 - self.hunger / 100))
        pygame.draw.line(screen, (255, 255, 0), pos, head)

        if self.posLastEaten != (0, 0):
            pygame.draw.circle(screen, (255, 0, 0), self.posLastEaten, 100)
            self.posLastEaten = (0, 0)

    def update(self, entities, scaryblobs, jaws):
        if self.hunger > 100:
            self.die()

        self.getFriends2(jaws)

        _group = self.groupWithFriends()
        _align = self.alignOnFriends()
        _dodge = self.dodgeFriends()
        _scare = self.dodgeScary(scaryblobs)
        _edges = self.dodgeEdges()
        _food = self.seekFood(entities)

        _group.multiply(0.1)

        if _group.getNorm() > 0: self.speed_.add(_group)
        if _align.getNorm() > 0: self.speed_.add(_align)
        if _dodge.getNorm() > 0: self.speed_.add(_dodge)
        if _scare.getNorm() > 0: self.speed_.add(_scare)
        if _edges.getNorm() > 0: self.speed_.add(_edges)
        if _food.getNorm() > 0 and self.hunger >= EATING_TRIGGER:
            _food.multiply(2 * self.hunger / 100)
            self.speed_.add(_food)
        self.hunger += max(0, gauss(0, 0.3))

        self.addNoise()
        self.limitSpeed(self.MAX_SPEED + 3 * self.hunger / 100)  # hungrier -> faster speed

        self.move()
        self.warpOnEdges()

    def seekFood(self, food):
        total = myVector(0, 0)
        if len(food) == 0: return total
        for f in food:
            pos = f.getPos()
            d = self.distance(pos)
            if d < self.EAT_RADIUS and self.hunger >= EATING_TRIGGER:
                f.die()
                self.hunger = max(0, self.hunger - EATING_AMOUNT)
                self.posLastEaten = pos
            if self.VISION_RADIUS > d > 0:
                vect = myVector(pos[0] - self.position_[0], pos[1] - self.position_[1])
                vect.multiply(1 / d)
                total.add(vect)
        total.normalize()
        return total
