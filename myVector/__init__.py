#
from numpy.linalg import norm
from math import atan2, pi, sin, cos

class myVector:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def add(self, vector):
        self.x  += vector.x
        self.y  += vector.y
        
    def getNorm(self):
        return norm([self.x, self.y])
    
    def multiply(self, value):
        self.x *= value
        self.y *= value
        
    def normalize(self):
        if self.getNorm() == 0 : 
            return myVector(0,0)
        else :
            self.multiply(1/self.getNorm())
        
    def getAngle(self):
        return - atan2(self.y, self.x)*180/pi
    
    def rotate(self, angle):
        angle = - angle * pi / 180
        old_x = self.x
        old_y = self.y
        self.x = cos(angle)*old_x - sin(angle)*old_y
        self.y = sin(angle)*old_x + cos(angle)*old_y
        
    def array(self):
        return [self.x, self.y]
    
    def display(self) :
        print("x:",self.x,"\ty:",self.y,
              "\nangle:", self.getAngle(), "\tnorm :", self.getNorm() )
