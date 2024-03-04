from characters.player import Player
from characters.utils.heart_item import HeartItem
from characters.utils.item import Item

# ゲームの共通設定が格納されているモジュール
from common.common import Common

import random

window_size = Common().get_window_size()

ITEM_DROP_SPEED = 3


class ItemObserver:
    def __init__(self):
        self.items = []

    def items_collided(self, item, player: Player):
        self.items.remove(item)
        item.use(player)

    def add_item(self):
        x = random.randint(0, window_size.width)
        y = 0
        heart_item = HeartItem(x, y)
        self.items.append(heart_item)

    def drop_items(self, player):
        for item in self.items:
            item.rect.y += ITEM_DROP_SPEED
            if item.rect.bottom > window_size.height:
                self.items.remove(item)
                break
            if item.rect.colliderect(player) and type(item) == HeartItem:
                self.items_collided(item, player)
                break
