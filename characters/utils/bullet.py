import pygame
from pygame.locals import *

#弾の設定を読み込むためのモジュール
from dotenv import load_dotenv
import os
load_dotenv()

BULLET_WIDTH = int(os.getenv('BULLET_WIDTH'))
BULLET_HEIGHT = int(os.getenv('BULLET_HEIGHT'))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_x, bullet_y, rotate=0):
        super().__init__()
        self._bullet_img = pygame.image.load("images/{}".format(os.getenv('BULLET_IMAGE')))
        self.image = pygame.transform.scale(self._bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect = pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT)