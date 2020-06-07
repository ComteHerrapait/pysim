import pygame

class ScaryBlob:
    
    def __init__(self, pos):
        """constructor"""
        self.position = pos
    
    def display(self, screen):
        pygame.draw.circle(screen, (255,0,255), self.position, 10)