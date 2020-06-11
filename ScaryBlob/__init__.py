import pygame

class ScaryBlob:
    
    def __init__(self, pos):
        """constructor"""
        self.position = pos
        self.DEATH_ZONE = 20
    
    def display(self, screen):
        pygame.draw.circle(screen, (255,0,255), self.position, 10)