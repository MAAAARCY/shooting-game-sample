import pygame
from pygame.locals import *

# ゲームの共通設定が格納されているモジュール
from common.common import Common

# 弾の設定を読み込むためのモジュール
from dotenv import load_dotenv
import os
load_dotenv()

window_size = Common().get_window_size()

HEART_WIDTH = int(os.getenv('HEART_WIDTH'))
HEART_HEIGHT = int(os.getenv('HEART_HEIGHT'))
HEART_X = 0
HEART_Y = window_size.height - HEART_HEIGHT


class Heart(pygame.sprite.Sprite):
    def __init__(self, heart_x):
        super().__init__()
        self._heart_img = pygame.image.load(
            "images/{}".format(os.getenv('PLAYER_HEART_IMAGE')))
        self.image = pygame.transform.scale(
            self._heart_img, (HEART_WIDTH, HEART_HEIGHT))
        self.rect = pygame.Rect(
            HEART_X+heart_x, HEART_Y, HEART_WIDTH, HEART_HEIGHT)
