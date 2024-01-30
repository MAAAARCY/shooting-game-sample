import pygame
from pygame.locals import *

BULLET_WIDTH = 20
BULLET_HEIGHT = 20

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_x, bullet_y, rotate=0):
        super().__init__()
        self._bullet_img = pygame.image.load("images/銃弾.png")
        self.image = pygame.transform.scale(self._bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect = pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT)