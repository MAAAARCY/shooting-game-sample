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

player_img = pygame.image.load("images/戦車_ver1.1.png")

# プレイヤーが打つ弾の設定
PLAYER_BULLET_WIDTH = 20
PLAYER_BULLET_HEIGHT = 20
PLAYER_BULLET_X = PLAYER_X
PLAYER_BULLET_Y = PLAYER_Y
PLAYER_BULLET_SPEED = 5
PLAYER_BULLET_MAX_COUNT = 2

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

enemy_bullet_img = pygame.image.load("images/銃弾.png")
reborn_time = 3

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
        #self.bullets = []
    
    def set_enemys(self):
        for i in range(ENEMY_MAX_COUNT):
            enemy = Enemy(ENEMY_BULLET_CYCLE + i)
            self.enemys.append(enemy)
    
    def move_x(self):
        for enemy in self.enemys:
            enemy.move_x()
    
    def shot_bullets(self, once:bool):
        if once == False: return

        for enemy in self.enemys:
            enemy.shot_bullet()
            #self.bullets.append(enemy.bullets)
    
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
once = True

#エネミーの弾の発射処理

player = Player()
enemy_operator = EnemyOperator()
enemy_operator.set_enemys()

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
        enemy_operator.shot_bullets(once)
        once = False
    else:
        once = True
    
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