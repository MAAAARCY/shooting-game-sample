import pygame
from pygame.locals import *
import random

# ゲームの共通設定が格納されているモジュール
from common.common import Common

# プレイヤーの情報が格納されているモジュール
from .player import Player

# 弾丸の情報が格納されているモジュール
from .utils.bullet import Bullet

# エネミー設定を読み込むためのモジュール
from dotenv import load_dotenv
import os
load_dotenv()

window_size = Common().get_window_size()

# エネミー設定
ENEMY_WIDTH = int(os.getenv('ENEMY_WIDTH')) * 3  # 幅
ENEMY_HEIGHT = int(os.getenv('ENEMY_HEIGHT')) * 3  # 高さ
ENEMY_X = window_size.width // 2  # X座標
ENEMY_Y = window_size.height // 2 - 250  # Y座標
ENEMY_SPEED_X = int(os.getenv('ENEMY_SPEED_X'))  # 移動速度
ENEMY_MAX_COUNT = int(os.getenv('ENEMY_MAX_COUNT'))  # 最大数
ENEMY_GENERATE_CYCLE = int(os.getenv('ENEMY_GENERATE_CYCLE'))  # エネミーが復活する周期
ENEMY_HEART = int(os.getenv('ENEMY_HEART'))+10  # エネミーの体力

ENEMY_BULLET_SPEED = int(os.getenv('ENEMY_BULLET_SPEED'))  # 弾の速度
ENEMY_BULLET_MAX_COUNT = 3  # 打てる弾の最大数
ENEMY_BULLET_CYCLE = int(os.getenv('ENEMY_BULLET_CYCLE'))


class BossEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._boss_enemy_img = pygame.image.load(
            "images/{}".format(os.getenv('ENEMY_IMAGE')))
        self._x = ENEMY_X
        self._y = ENEMY_Y
        self.image = pygame.transform.scale(
            self._boss_enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = pygame.Rect(self._x, self._y, ENEMY_WIDTH, ENEMY_HEIGHT)

        self.speed_x = random.randint(ENEMY_SPEED_X, ENEMY_SPEED_X+5)
        self.bullet_cycle = ENEMY_BULLET_CYCLE
        self.bullet_speed = ENEMY_BULLET_SPEED
        self.heart = ENEMY_HEART * 2
        self.bullets = []

        self.name = "Boss"

    def move_x(self):
        self.rect.x += self.speed_x

        # エネミーが画面外に出ないようにするための処理
        if self.rect.left < 0 or self.rect.right > window_size.width:
            self.speed_x = -self.speed_x

    def shot_bullet(self):
        enemy_bullet_x = self.rect.x + ENEMY_WIDTH // 2
        enemy_bullet_y = self.rect.y

        bullet = Bullet(enemy_bullet_x, enemy_bullet_y, 180)
        self.bullets.append(bullet)
        # self.bullet_cycle += ENEMY_BULLET_CYCLE

    def bullet_collided(self, player: Player):
        for bullet in self.bullets:
            bullet.rect.y += ENEMY_BULLET_SPEED
            # 弾が画面外に出た時の処理
            if bullet.rect.top > window_size.height:
                self.bullets.remove(bullet)
            # プレイヤーに弾が当たった時の処理
            if bullet.rect.colliderect(player):
                self.bullets.remove(bullet)
                return True

        return False
