#
from numpy.linalg import norm

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
        self.multiply(1/self.getNorm())