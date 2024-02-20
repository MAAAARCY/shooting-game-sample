from ..utils.bullet import Bullet
import pygame
from pygame.locals import *

# 弾の設定を読み込むためのモジュール
from dotenv import load_dotenv
import os
load_dotenv()

BULLET_WIDTH = int(os.getenv('BULLET_WIDTH'))
BULLET_HEIGHT = int(os.getenv('BULLET_HEIGHT'))


class SpecialBullet(Bullet):
    def __init__(self, bullet_x: int, bullet_y: int):
        super().__init__(bullet_x, bullet_y)
        self.image = pygame.transform.scale(
            self._bullet_img, (BULLET_WIDTH*10, BULLET_HEIGHT*10))
        self.rect = pygame.Rect(
            bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT)
