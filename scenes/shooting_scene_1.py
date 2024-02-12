import pygame
from pygame.locals import *
import sys

import random

from common.common import Common

from characters.player import Player

from observers.enemy_observer import EnemyObserver

from text_components.score import Score

BOSS_BULLET_CYCLE = 1
ENEMY_BULLET_CYCLE = 1
GENERATE_ENEMY_CYCLE = 1


class Shooting_scene_1:
    def scene(self, screen, clock, fps):
        player = Player()
        enemy_operator = EnemyObserver()
        enemy_operator.set_enemy()

        score = Score()
        time_keeper = Common().get_time_keeper(
            generate_enemy_cycle=GENERATE_ENEMY_CYCLE,
            enemy_bullet_cycle=ENEMY_BULLET_CYCLE,
            boss_bullet_cycle=BOSS_BULLET_CYCLE
        )

        kill_enemy_count = 0  # エネミーを倒した数

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

            # 時間管理
            time_keeper.add_frame_time(clock.get_time())  # フレーム時間を足す

            # 移動処理
            # プレイヤーの移動
            player.move_x(keys)

            # エネミーの移動
            enemy_operator.move_x()

            # 弾の挙動に関する処理
            # プレイヤーの弾の当たり判定
            if player.bullet_collided(enemy_operator, score):
                kill_enemy_count += 1
            if kill_enemy_count == 10:
                enemy_operator.set_boss()

            # エネミーの弾の当たり判定
            enemy_operator.bullets_collided(player)
            if len(enemy_operator.bosses) != 0:
                enemy_operator.bosses[0].bullet_collided(player)

            # エネミーの弾発射周期管理
            if time_keeper.now_second % time_keeper.enemy_bullet_cycle == 0 and time_keeper.now_second != 0:
                pick_num = random.randint(0, len(enemy_operator.enemys))

                enemy_operator.shot_bullets(pick_num)
                time_keeper.add_enemy_bullet_cycle(ENEMY_BULLET_CYCLE)

            # ボスの弾発射周期管理
            if time_keeper.now_milli_second % time_keeper.boss_bullet_cycle == 0 and time_keeper.now_second != 0:
                if len(enemy_operator.bosses) != 0:
                    enemy_operator.bosses[0].shot_bullet()
                time_keeper.add_boss_bullet_cycle(0.5)

            # 死んだエネミーを復活させる処理
            if time_keeper.reborn_second % time_keeper.generate_enemy_cycle == 0 and time_keeper.reborn_second != 0:
                enemy_operator.set_enemy()
                time_keeper.add_generate_enemy_cycle(GENERATE_ENEMY_CYCLE)

            # 以下描画処理
            all_sprites = pygame.sprite.Group()
            # プレイヤーを描画
            all_sprites.add(player)

            # エネミーを描画
            all_sprites.add(enemy_operator.enemys)
            # プレイヤーの弾を描画
            all_sprites.add(player.bullets)

            # エネミーの弾を描画
            for enemy in enemy_operator.enemys:
                all_sprites.add(enemy.bullets)\

            # スコアを描画
            score_surface = score.font.render(
                "Score: " + str(score.score), True, (0, 0, 0)
            )
            screen.blit(score_surface, (10, 10))

            all_sprites.draw(screen)

            pygame.display.update()
            clock.tick(fps)
