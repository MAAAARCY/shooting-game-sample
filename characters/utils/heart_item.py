from ..utils.item import Item
import pygame
from pygame.locals import *

# プレイヤーの情報が格納されているモジュール
from characters.player import Player

from ..utils.heart import Heart

# 弾の設定を読み込むためのモジュール
from dotenv import load_dotenv
import os
load_dotenv()

ITEM_WIDTH = int(os.getenv('ITEM_WIDTH'))
ITEM_HEIGHT = int(os.getenv('ITEM_HEIGHT'))


class HeartItem(Item):
    def __init__(self, item_x: int, item_y: int):
        super().__init__(item_x, item_y)
        self._item_img = pygame.image.load(
            "images/{}".format(os.getenv('HEART_IMAGE')))
        self.image = pygame.transform.scale(
            self._item_img, (ITEM_WIDTH, ITEM_HEIGHT))
        self.rect = pygame.Rect(
            item_x, item_y, ITEM_WIDTH, ITEM_HEIGHT)

    def use(self, player: Player):
        player_max_heart = int(os.getenv("PLAYER_HEART"))

        for i in range(max(player_max_heart - player.heart, 0)):
            heart = Heart((i + player.heart)*int(os.getenv('HEART_WIDTH')))
            player.hearts.append(heart)

        player.heart = int(os.getenv("PLAYER_HEART"))
