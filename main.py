import pygame
from pygame.locals import *
import sys

from common.common import Common

from characters.player import Player

from observers.enemy_observer import EnemyObserver

from text_components.score import Score

pygame.init()
clock = pygame.time.Clock()

score = Score()

fps = Common().get_fps()
window_size = Common().get_window_size()

screen = pygame.display.set_mode((window_size.width, window_size.height))
pygame.display.set_caption('シューティングゲーム')

# 時間管理
now_time = 0
reborn_time = 0
once = True

player = Player()
enemy_operator = EnemyObserver()
enemy_operator.set_enemy()

score = Score()

ENEMY_BULLET_CYCLE = 1
ENEMY_GENERATE_CYCLE = 1

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
                player.shot_bullet()
    
    # キーボードの状態を取得
    keys = pygame.key.get_pressed()

    # 移動処理
    # プレイヤーの移動
    player.move_x(keys)
    
    # エネミーの移動
    enemy_operator.move_x()
    
    # 弾の挙動に関する処理
    # プレイヤーの弾の当たり判定
    player.bullet_collided(enemy_operator, score)
    
    # エネミーの弾の当たり判定
    enemy_operator.bullets_collided(player)
    
    # エネミーの弾発射周期管理
    if (now_time // 1000) % ENEMY_BULLET_CYCLE == 0 and (now_time // 1000) != 0:
        enemy_operator.shot_bullets()
        ENEMY_BULLET_CYCLE += 1
        if ENEMY_BULLET_CYCLE > 10:
            ENEMY_BULLET_CYCLE = 1
            now_time = 0
    
    # 死んだエネミーを復活させる処理
    if (reborn_time // 1000) % ENEMY_GENERATE_CYCLE == 0 and (reborn_time // 1000) != 0:
        #print("reborn")
        enemy_operator.set_enemy()
        ENEMY_GENERATE_CYCLE += 1
        if ENEMY_GENERATE_CYCLE > 10:
            ENEMY_GENERATE_CYCLE = 1
            reborn_time = 0
    
    # 以下描画処理
    all_sprites = pygame.sprite.Group()
    # プレイヤーを描画
    all_sprites.add(player)
    
    # エネミーを描画
    all_sprites.add(enemy_operator.enemys)
    # プレイヤーの弾を描画
    all_sprites.add(player.bullets)
    
    # エネミーの弾を描画
    #all_sprites.add(enemy_operator.bullets)
    for enemy in enemy_operator.enemys:
        all_sprites.add(enemy.bullets)
    # スコアを描画
    score_surface = score.font.render("Score: " + str(score.score), True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    all_sprites.draw(screen)

    pygame.display.update()
    clock.tick(fps)
    now_time += clock.get_time()
    reborn_time += clock.get_time()