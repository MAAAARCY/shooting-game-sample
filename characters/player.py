import pygame
from pygame.locals import *

#ゲームの共通設定が格納されているモジュール
from common.common import Common

#弾丸の情報が格納されているモジュール
from .utils.bullet import Bullet

window_size = Common().get_window_size()

# プレイヤー設定
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 60
PLAYER_X = (window_size.width - PLAYER_WIDTH) // 2
PLAYER_Y = window_size.height - 100
PLAYER_SPEED_X = 5

PLAYER_BULLET_SPEED = 5
PLAYER_BULLET_MAX_COUNT = 3

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._player_img = pygame.image.load("images/戦車_ver1.1.png")
        self.image = pygame.transform.scale(self._player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        self.bullets = []
        print("X:{},Y:{}".format(self.rect.x, self.rect.y))
    
    def move_x(self, keys):
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED_X
        if keys[K_RIGHT] and self.rect.right < window_size.width:
            self.rect.x += PLAYER_SPEED_X
    
    #プレイヤーの弾の発射処理
    def shot_bullet(self):
        if PLAYER_BULLET_MAX_COUNT > len(self.bullets):
            player_bullet_x = self.rect.x + PLAYER_WIDTH // 2
            player_bullet_y = self.rect.y # 元々はPLAYER_BULLET_Y
            player_bullet = Bullet(player_bullet_x, player_bullet_y)
            
            self.bullets.append(player_bullet)
    
    #プレイヤーの弾の当たり判定
    def bullet_collided(self, enemy_operator, score):
        for bullet in self.bullets:
            bullet.rect.y -= PLAYER_BULLET_SPEED
            # 弾が画面外に出た時の処理
            if bullet.rect.top < 0:
                self.bullets.remove(bullet)
            # エネミーに弾が当たった時の処理
            for enemy in enemy_operator.enemys:
                if bullet.rect.colliderect(enemy):
                    if type(bullet) == Bullet: self.bullets.remove(bullet)

                    enemy.heart -= 1
                    if enemy.heart == 0: enemy_operator.enemys.remove(enemy)
                    score.score += 10