import pygame
from pygame.locals import *

import random

from characters.player import Player
from characters.enemy import Enemy

ENEMY_MAX_COUNT = 10 #エネミーの最大数

class EnemyObserver:
    def __init__(self):
        self.enemys = []
        self.enemys_stock = []
    
    def set_enemy(self):
        enemy = Enemy()

        if len(self.enemys) < ENEMY_MAX_COUNT: self.enemys.append(enemy)

    def set_enemys(self):
        for i in range(ENEMY_MAX_COUNT):
            enemy = Enemy()
            self.enemys.append(enemy)
    
    def move_x(self):
        for enemy in self.enemys:
            enemy.move_x()
    
    def shot_bullets(self):
        pick_num = random.randint(0, len(self.enemys))

        for enemy_num, enemy in enumerate(self.enemys):
            if enemy_num == pick_num:
                enemy.shot_bullet()
    
    def bullets_collided(self, player:Player):
        for enemy in self.enemys:
            enemy.bullet_collided(player)