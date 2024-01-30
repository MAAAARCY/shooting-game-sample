import pygame
from pygame.locals import *
import random

#ゲームの共通設定が格納されているモジュール
from common.common import Common

#プレイヤーの情報が格納されているモジュール
from .player import Player

#弾丸の情報が格納されているモジュール
from .utils.bullet import Bullet

window_size = Common().get_window_size()

# エネミー設定
ENEMY_WIDTH = 80 #幅 
ENEMY_HEIGHT = 60 #高さ
ENEMY_X = window_size.width // 2 #X座標
ENEMY_Y = window_size.height // 2 #Y座標
ENEMY_SPEED_X = 5 #移動速度
ENEMY_MAX_COUNT = 5 #最大数
ENEMY_GENERATE_CYCLE = 2 #エネミーが復活する周期

ENEMY_BULLET_SPEED = 5 #弾の速度
ENEMY_BULLET_MAX_COUNT = 3 #打てる弾の最大数
ENEMY_BULLET_CYCLE = 3

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._enemy_img = pygame.image.load("images/UFO.png")
        self._x = random.randint(0, ENEMY_X)
        self._y = random.randint(0, ENEMY_Y)
        self.image = pygame.transform.scale(self._enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = pygame.Rect(self._x, self._y, ENEMY_WIDTH, ENEMY_HEIGHT)

        self.speed_x = random.randint(ENEMY_SPEED_X, ENEMY_SPEED_X+5)
        self.bullet_cycle = ENEMY_BULLET_CYCLE
        self.bullet_speed = ENEMY_BULLET_SPEED
        self.bullets = []
    
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
        #self.bullet_cycle += ENEMY_BULLET_CYCLE

    def bullet_collided(self, player:Player):
        for bullet in self.bullets:
            bullet.rect.y += ENEMY_BULLET_SPEED
            # 弾が画面外に出た時の処理
            if bullet.rect.top > window_size.height:
                self.bullets.remove(bullet)
            # プレイヤーに弾が当たった時の処理
            if bullet.rect.colliderect(player):
                self.bullets.remove(bullet)