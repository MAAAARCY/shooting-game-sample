import pygame
from pygame.locals import *

# 弾の設定を読み込むためのモジュール
from dotenv import load_dotenv
import os
load_dotenv()

ITEM_WIDTH = int(os.getenv('ITEM_WIDTH'))
ITEM_HEIGHT = int(os.getenv('ITEM_HEIGHT'))


class Item(pygame.sprite.Sprite):
    def __init__(self, item_x: int, item_y: int, rotate=0):
        super().__init__()
        self._item_img = pygame.image.load(
            "images/{}".format(os.getenv('HEART_IMAGE')))
        self.image = pygame.transform.scale(
            self._item_img, (ITEM_WIDTH, ITEM_HEIGHT))
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect = pygame.Rect(
            item_x, item_y, ITEM_WIDTH, ITEM_HEIGHT)
