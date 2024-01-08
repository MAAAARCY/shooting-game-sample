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
PLAYER_HEIGHT = 60
PLAYER_X = (WINDOW_WIDTH - PLAYER_WIDTH) // 2
PLAYER_Y = WINDOW_HEIGHT - 100
PLAYER_SPEED_X = 5

player_img = pygame.image.load("images/戦車.png")
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
player = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)

# プレイヤーが打つ弾の設定
PLAYER_BULLET_WIDTH = 20
PLAYER_BULLET_HEIGHT = 20
PLAYER_BULLET_X = PLAYER_X
PLAYER_BULLET_Y = PLAYER_Y
PLAYER_BULLET_SPEED = 5
PLAYER_BULLET_MAX_COUNT = 5

#player_bullet = pygame.Rect(PLAYER_BULLET_X, PLAYER_BULLET_Y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)\
player_bullet_img = pygame.image.load("images/銃弾.png")
player_bullet_img = pygame.transform.scale(player_bullet_img, (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))
player_bullets = []

# エネミー設定
ENEMY_WIDTH = 80
ENEMY_HEIGHT = 60
ENEMY_X = WINDOW_WIDTH // 2
ENEMY_Y = WINDOW_HEIGHT // 2
ENEMY_SPEED_X = 5
ENEMY_MAX_COUNT = 5

enemy_img = pygame.image.load("images/UFO.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))

# エネミーが打つ弾の設定
ENEMY_BULLET_WIDTH = 20
ENEMY_BULLET_HEIGHT = 20
ENEMY_BULLET_X = ENEMY_X
ENEMY_BULLET_Y = ENEMY_Y
ENEMY_BULLET_SPEED = 5
ENEMY_BULLET_CYCLE = 3 #秒数指定
ENEMY_BULLET_MAX_COUNT = 5

#enemy = pygame.Rect(ENEMY_X, ENEMY_Y, ENEMY_WIDTH, ENEMY_HEIGHT)
enemy_bullet_img = pygame.image.load("images/銃弾.png")
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT))
enemy_bullet_img = pygame.transform.rotate(enemy_bullet_img, 180)
enemys = []
enemys_speed_x = []
enemys_bullet_cycle = []
enemys_bullets = []
enemys_bullet_speed = []
#kill_enemys = []
reborn_time = 3
for i in range(ENEMY_MAX_COUNT):
    enemy_x = random.randint(0, ENEMY_X)
    enemy_y = random.randint(0, ENEMY_Y)
    enemy = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)
    enemys.append(enemy)
    enemys_speed_x.append(random.randint(ENEMY_SPEED_X, ENEMY_SPEED_X+5))
    enemys_bullet_cycle.append(ENEMY_BULLET_CYCLE + i)
    enemys_bullet_speed.append(ENEMY_BULLET_SPEED)

# スコア
score = 0
font = pygame.font.Font(None, 30)

# 時間管理
now_time = 0

#プレイヤーの弾の発射処理
def shot_bullet_by_player():
    if PLAYER_BULLET_MAX_COUNT > len(player_bullets):
        player_bullet_x = player.x + PLAYER_WIDTH // 2
        player_bullet_y = PLAYER_BULLET_Y
        player_bullet = pygame.Rect(player_bullet_x, player_bullet_y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
        player_bullets.append(player_bullet)

#エネミーの弾の発射処理
def shot_bullet_by_enemy(enemy_num:int):
    if ENEMY_BULLET_MAX_COUNT > len(enemys_bullets):
        enemy_bullet_x = enemys[enemy_num].x + ENEMY_WIDTH // 2
        enemy_bullet_y = enemys[enemy_num].y
        enemy_bullet = pygame.Rect(enemy_bullet_x, enemy_bullet_y, ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT)
        enemys_bullets.append(enemy_bullet)
        enemys_bullet_cycle[enemy_num] += ENEMY_BULLET_CYCLE

while True:
    # ウインドウを白で塗りつぶす
    screen.fill((255, 255, 255))

    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                shot_bullet_by_player()
    
    # キーボードの状態を取得
    keys = pygame.key.get_pressed()

    # 移動処理
    # プレイヤーの移動
    if keys[K_LEFT] and player.left > 0:
        player.x -= PLAYER_SPEED_X
    if keys[K_RIGHT] and player.right < WINDOW_WIDTH:
        player.x += PLAYER_SPEED_X
    
    # エネミーの移動
    for enemy_num, enemy in enumerate(enemys):
        enemy.x += enemys_speed_x[enemy_num]

        # エネミーが画面外に出ないようにするための処理
        if enemy.left < 0 or enemy.right > WINDOW_WIDTH:
            enemys_speed_x[enemy_num] = -enemys_speed_x[enemy_num]
    
    # 弾の挙動に関する処理
    # プレイヤーの弾の当たり判定
    for bullet in player_bullets:
        bullet.y -= PLAYER_BULLET_SPEED
        # 弾が画面外に出た時の処理
        if bullet.top < 0:
            player_bullets.remove(bullet)
        # エネミーに弾が当たった時の処理
        for enemy_num, enemy in enumerate(enemys):
            if bullet.colliderect(enemy):
                player_bullets.remove(bullet)
                enemys.remove(enemy)

                del enemys_bullet_cycle[enemy_num]
                #del enemys_bullet_speed[enemy_num]
                #del enemys_speed_x[enemy_num]
                score += 10
    
    # エネミーの弾の当たり判定
    for enemy_num, bullet in enumerate(enemys_bullets):
        bullet.y += enemys_bullet_speed[enemy_num]
        # 弾が画面外に出た時の処理
        if bullet.top > WINDOW_HEIGHT:
            enemys_bullets.remove(bullet)
        # プレイヤーに弾が当たった時の処理
        if bullet.colliderect(player):
            enemys_bullets.remove(bullet)
            score -= 10
    
    # エネミーの弾発射周期管理
    for enemy_num, cycle in enumerate(enemys_bullet_cycle):
        if (now_time // 1000) % cycle == 0 and (now_time // 1000) != 0:
            print(cycle)
            enemys_bullet_cycle[enemy_num] += ENEMY_BULLET_CYCLE
            shot_bullet_by_enemy(enemy_num)
            print(len(enemys_bullets))
    
    # 死んだエネミーを復活させる処理
    """
    if (now_time // 1010) % 10 == 0 and len(enemys) != ENEMY_MAX_COUNT:
        print("reborn")
        enemy_x = random.randint(0, ENEMY_X)
        enemy_y = random.randint(0, ENEMY_Y)
        enemy = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)
        enemys.append(enemy)
        enemys_speed_x.append(random.randint(ENEMY_SPEED_X, ENEMY_SPEED_X+5))
        enemys_bullet_cycle.append(ENEMY_BULLET_CYCLE)
        enemys_bullet_speed.append(ENEMY_BULLET_SPEED)
    """
    # 以下描画処理
    # プレイヤーを描画
    #pygame.draw.rect(screen, (0, 0, 0), player)
    screen.blit(player_img, player)

    # エネミーを描画
    for enemy in enemys:
        #pygame.draw.rect(screen, (0, 0, 0), enemy)
        screen.blit(enemy_img, enemy)

    # プレイヤーの弾を描画
    for bullet in player_bullets:
        #pygame.draw.rect(screen, (0, 0, 0), bullet)
        screen.blit(player_bullet_img, bullet)
    
    # エネミーの弾を描画
    for bullet in enemys_bullets:
        #pygame.draw.rect(screen, (0, 0, 0), bullet)
        screen.blit(enemy_bullet_img, bullet)
    
    # スコアを描画
    score_surface = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    pygame.display.update()
    clock.tick(FPS)
    now_time += clock.get_time()