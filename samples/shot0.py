import pygame
from pygame.locals import *
import sys

import random

pygame.init()
clock = pygame.time.Clock()

FPS = 60

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('シューティングゲーム')

# プレイヤー設定
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 10
PLAYER_X = (WINDOW_WIDTH - PLAYER_WIDTH) // 2
PLAYER_Y = WINDOW_HEIGHT - 50
PLAYER_SPEED_X = 5

player = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)

# プレイヤーが打つ弾の設定
PLAYER_BULLET_WIDTH = 5
PLAYER_BULLET_HEIGHT = 5
PLAYER_BULLET_X = PLAYER_X
PLAYER_BULLET_Y = PLAYER_Y
PLAYER_BULLET_SPEED = 5
PLAYER_BULLET_MAX_COUNT = 5

#player_bullet = pygame.Rect(PLAYER_BULLET_X, PLAYER_BULLET_Y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
player_bullets = []

# エネミー設定
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
ENEMY_X = WINDOW_WIDTH // 2
ENEMY_Y = WINDOW_HEIGHT // 2
ENEMY_SPEED_X = 5
ENEMY_MAX_COUNT = 3

#enemy = pygame.Rect(ENEMY_X, ENEMY_Y, ENEMY_WIDTH, ENEMY_HEIGHT)
enemys = []
enemys_speed_x = []
for i in range(ENEMY_MAX_COUNT):
    enemy_x = random.randint(0, ENEMY_X)
    enemy_y = random.randint(0, ENEMY_Y)
    enemy = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)
    enemys.append(enemy)
    enemys_speed_x.append(ENEMY_SPEED_X)

#プレイヤーの弾を補充する際に実行する関数
def shot_bullet_by_player():
    if PLAYER_BULLET_MAX_COUNT > len(player_bullets):
        player_bullet_x = player.x + PLAYER_WIDTH // 2
        player_bullet_y = PLAYER_BULLET_Y
        player_bullet = pygame.Rect(player_bullet_x, player_bullet_y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
        player_bullets.append(player_bullet)

while True:
    # ウインドウを白で塗りつぶす
    screen.fill((255, 255, 255))

    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE: #おまけ課題
                shot_bullet_by_player()
    
    # キーボードの状態を取得
    keys = pygame.key.get_pressed()

    # 移動処理
    # プレイヤーの移動
    if keys[K_LEFT] and """問題1(1)""":
        player.x -= PLAYER_SPEED_X
    if keys[K_RIGHT] and """問題1(2)""":
        player.x += PLAYER_SPEED_X
    
    # エネミーの移動
    for enemy_num, enemy in enumerate(enemys):
        enemy.x += enemys_speed_x[enemy_num]

        # エネミーが画面外に出ないようにするための処理
        if """問題2(1)""" or """問題2(2)""":
            enemys_speed_x[enemy_num] = -enemys_speed_x[enemy_num]
    
    # 弾の挙動に関する処理
    # 発射処理
    for bullet in player_bullets:
        bullet.y -= PLAYER_BULLET_SPEED
        #弾が画面外に出た時の処理
        if """問題3""":
            player_bullets.remove(bullet)
        # エネミーに弾が当たった時の処理
        for enemy in enemys:
            if bullet.colliderect(enemy):
                player_bullets.remove(bullet)
                enemys.remove(enemy)

    # 以下描画処理
    # プレイヤーを描画
    pygame.draw.rect(screen, (0, 0, 0), player)

    # エネミーを描画
    for enemy in enemys:
        pygame.draw.rect(screen, (0, 0, 0), enemy)

    # プレイヤーの弾を描画
    for bullet in player_bullets:
        pygame.draw.rect(screen, (0, 0, 0), bullet)

    pygame.display.update()
    clock.tick(FPS)