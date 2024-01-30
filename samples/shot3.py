import pygame
from pygame.locals import *
import sys

import random
import time

pygame.init()
clock = pygame.time.Clock()

FPS = 60

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('シューティングゲーム')

# プレイヤー設定
PLAYER_WIDTH = 80 #プレイヤーの幅
PLAYER_HEIGHT = 60 #プレやーの高さ
PLAYER_X = (WINDOW_WIDTH - PLAYER_WIDTH) // 2 #プレイヤーのX座標
PLAYER_Y = WINDOW_HEIGHT - 100 #プレイヤーのY座標
PLAYER_SPEED_X = 5 #プレイヤーの速度

player_img = pygame.image.load("images/戦車_ver1.1.png")

# プレイヤーが打つ弾の設定
PLAYER_BULLET_WIDTH = 20 #プレイヤー弾の幅
PLAYER_BULLET_HEIGHT = 20 #プレイヤー弾の高さ
PLAYER_BULLET_X = PLAYER_X #プレイヤー弾のX座標
PLAYER_BULLET_Y = PLAYER_Y #プレイヤー弾のY座標
PLAYER_BULLET_SPEED = 5 #プレイヤー弾の速度
PLAYER_BULLET_MAX_COUNT = 10 #プレイヤー弾の最大値

bullet_img = pygame.image.load("images/銃弾.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        self.bullets = []
    
    def move_x(self, keys):
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED_X
        if keys[K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += PLAYER_SPEED_X
    
    #プレイヤーの弾の発射処理
    def shot_bullet(self):
        if PLAYER_BULLET_MAX_COUNT > len(self.bullets):
            player_bullet_x = self.rect.x + PLAYER_WIDTH // 2
            player_bullet_y = PLAYER_BULLET_Y
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
                    self.bullets.remove(bullet)
                    enemy_operator.enemys.remove(enemy)
                    score.score += 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_x, bullet_y, rotate=0):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect = pygame.Rect(bullet_x, bullet_y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)

# エネミー設定
ENEMY_WIDTH = 80 #エネミーの幅
ENEMY_HEIGHT = 60 #エネミーの高さ
ENEMY_X = WINDOW_WIDTH // 2 #エネミーのX座標
ENEMY_Y = WINDOW_HEIGHT // 2 #エネミーのY座標
ENEMY_SPEED_X = 5 #エネミーのスピード
ENEMY_MAX_COUNT = 10 #エネミーの数の最大値
ENEMY_GENERATE_CYCLE = 2 #エネミーが生成される間隔の設定

enemy_img = pygame.image.load("images/UFO.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))

# エネミーが打つ弾の設定
ENEMY_BULLET_WIDTH = 20 #エネミー弾の幅
ENEMY_BULLET_HEIGHT = 20 #エネミー弾の高さ
ENEMY_BULLET_X = ENEMY_X #エネミー弾のX座標
ENEMY_BULLET_Y = ENEMY_Y #エネミー弾のY座標
ENEMY_BULLET_SPEED = 5 #エネミー弾の速さ
ENEMY_BULLET_CYCLE = 1 #エネミー弾を打つ間隔の設定
ENEMY_BULLET_MAX_COUNT = 5 #エネミー弾数の最大値

enemy_bullet_img = pygame.image.load("images/銃弾.png")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, bullet_cycle):
        super().__init__()
        enemy_x = random.randint(0, ENEMY_X)
        enemy_y = random.randint(0, ENEMY_Y)
        self.image = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)

        self.speed_x = random.randint(ENEMY_SPEED_X, ENEMY_SPEED_X+5)
        self.bullet_cycle = bullet_cycle
        self.bullet_speed = ENEMY_BULLET_SPEED
        self.bullets = []
    
    def move_x(self):
        self.rect.x += self.speed_x

        # エネミーが画面外に出ないようにするための処理
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.speed_x = -self.speed_x
    
    def shot_bullet(self):
        enemy_bullet_x = self.rect.x + ENEMY_WIDTH // 2
        enemy_bullet_y = self.rect.y

        bullet = Bullet(enemy_bullet_x, enemy_bullet_y, 180)
        self.bullets.append(bullet)
        self.bullet_cycle += ENEMY_BULLET_CYCLE

    def bullet_collided(self, player:Player):
        for bullet in self.bullets:
            bullet.rect.y += ENEMY_BULLET_SPEED
            # 弾が画面外に出た時の処理
            if bullet.rect.top > WINDOW_HEIGHT:
                self.bullets.remove(bullet)
            # プレイヤーに弾が当たった時の処理
            if bullet.rect.colliderect(player):
                self.bullets.remove(bullet)

class EnemyOperator:
    def __init__(self):
        self.enemys = []
        self.enemys_stock = []
        #self.bullets = []
    
    def set_enemy(self):
        enemy = Enemy(ENEMY_BULLET_CYCLE)

        if len(self.enemys) < ENEMY_MAX_COUNT: self.enemys.append(enemy)

    def set_enemys(self):
        for i in range(ENEMY_MAX_COUNT):
            enemy = Enemy(ENEMY_BULLET_CYCLE + i)
            #self.enemys.append(enemy)
            self.enemys.append(enemy)
        #enemy = Enemy(ENEMY_BULLET_CYCLE)
        #self.enemys.append(enemy)
    
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

# スコア
#score = 0
#font = pygame.font.Font(None, 30)

class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 30)

# 時間管理
now_time = 0
reborn_time = 0
once = True

#エネミーの弾の発射処理

player = Player()
enemy_operator = EnemyOperator()
enemy_operator.set_enemy()

score = Score()

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
        enemy_operator.set_enemy() #エネミーを一匹出現させる処理が入ってる
        ENEMY_GENERATE_CYCLE += 2
        if ENEMY_GENERATE_CYCLE > 10:
            ENEMY_GENERATE_CYCLE = 2
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
    clock.tick(FPS)
    now_time += clock.get_time()
    reborn_time += clock.get_time()