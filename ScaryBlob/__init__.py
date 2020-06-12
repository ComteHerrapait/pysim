import pygame

class ScaryBlob:
    
    def __init__(self, pos):
        """constructor"""
        self.position = pos
        self.DEATH_ZONE = 20
    
    def display(self, screen):
        pygame.draw.circle(screen, (155, 155, 155), self.position, 20)