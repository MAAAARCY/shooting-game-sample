import pygame
from pygame.locals import *

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

    def bullets_collided(self, player: Player):
        for enemy in self.enemys:
            enemy.bullet_collided(player)
