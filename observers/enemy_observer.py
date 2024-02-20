import pygame
from pygame.locals import *
import sys

import random

from characters.player import Player
from characters.enemy import Enemy
from characters.boss_enemy import BossEnemy

from dotenv import load_dotenv
import os
load_dotenv()

ENEMY_MAX_COUNT = int(os.getenv('ENEMY_MAX_COUNT'))  # エネミーの最大数
BOSS_MAX_COUNT = 1


class EnemyObserver:
    def __init__(self):
        self.enemys = []
        self.enemys_stock = []
        self.bosses = []
        self.all_enemys = []
        self.kill_enemy_count = 0

    def set_enemy(self):
        enemy = Enemy()

        if len(self.enemys) < ENEMY_MAX_COUNT:
            self.enemys.append(enemy)

    def set_enemys(self):
        for i in range(ENEMY_MAX_COUNT):
            enemy = Enemy()
            self.enemys.append(enemy)

    def set_boss(self):
        boss = BossEnemy()

        if len(self.bosses) < BOSS_MAX_COUNT:
            self.enemys.append(boss)

        self.bosses.append(boss)

    def move_x(self):
        for enemy in self.enemys:
            enemy.move_x()
        for boss in self.bosses:
            boss.move_x()

    def shot_bullets(self, pick_num):
        for enemy_num, enemy in enumerate(self.enemys):
            if enemy_num == pick_num:
                enemy.shot_bullet()

    def damage_enemy(self, enemy):
        enemy.heart -= 1

    def enemy_killed(self, score):
        for enemy in self.enemys:
            if enemy.heart == 0:
                self.enemys.remove(enemy)
                if enemy.name == "Enemy":
                    score.value += 10
                elif enemy.name == "Boss":
                    score.value += 100
                self._enemy_killed = True
                # pygame.time.wait(10)
                self.kill_enemy_count += 1
                break

            if enemy.name == "Boss":
                print("Boss Heart: {}".format(enemy.heart))

        if self.kill_enemy_count == 10:
            self.set_boss()

    def bullets_collided(self, player: Player):
        for enemy in self.enemys:
            if enemy.bullet_collided(player):
                player.heart -= 1
                player.hearts = player.hearts[0:player.heart]
                if player.heart == 0:
                    pygame.quit()
                    sys.exit()
