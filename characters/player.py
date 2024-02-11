import pygame
from pygame.locals import *

#ゲームの共通設定が格納されているモジュール
from common.common import Common

#弾丸の情報が格納されているモジュール
from .utils.bullet import Bullet

#プレイヤー設定を読み込むためのモジュール
from dotenv import load_dotenv
import os
load_dotenv()

window_size = Common().get_window_size()

# プレイヤー設定
PLAYER_WIDTH = int(os.getenv('PLAYER_WIDTH'))
PLAYER_HEIGHT = int(os.getenv('PLAYER_HEIGHT'))
PLAYER_X = (window_size.width - PLAYER_WIDTH) // 2
PLAYER_Y = window_size.height - 100
PLAYER_SPEED_X = int(os.getenv('PLAYER_SPEED_X'))

PLAYER_BULLET_SPEED = int(os.getenv('PLAYER_BULLET_SPEED'))
PLAYER_BULLET_MAX_COUNT = int(os.getenv('PLAYER_BULLET_MAX_COUNT'))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._player_img = pygame.image.load("images/{}".format(os.getenv('PLAYER_IMAGE')))
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
        flag = False
        for bullet in self.bullets:
            bullet.rect.y -= PLAYER_BULLET_SPEED
            # 弾が画面外に出た時の処理
            if bullet.rect.top < 0:
                self.bullets.remove(bullet)
            # エネミーに弾が当たった時の処理
            for enemy in enemy_operator.enemys:
                if bullet.rect.colliderect(enemy):
                    self.bullets.remove(bullet)

                    enemy.heart -= 1
                    if enemy.heart == 0: 
                        enemy_operator.enemys.remove(enemy)
                        score.score += 10
                        flag = True
                        break
            
            if flag: break

            for boss in enemy_operator.bosses:
                if bullet.rect.colliderect(boss):
                    self.bullets.remove(bullet)

                    boss.heart -= 1
                    if boss.heart == 0:
                        enemy_operator.bosses.remove(boss)
                        score.score += 100
                        flag = True
            
            if flag: break

        return flag