import pygame
from pygame.locals import *

class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 30)