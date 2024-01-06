import pygame
from pygame.locals import *
import sys
import time

pygame.init()
clock = pygame.time.Clock()

FPS = 60

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('ブロック崩し')

# パドル
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
PADDLE_X = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
PADDLE_Y = WINDOW_HEIGHT - 50

paddle = pygame.Rect(PADDLE_X, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

# ボール
BALL_WIDTH = 10 # ボールの幅
BALL_HEIGHT = 10 # ボールの高さ
BALL_X = WINDOW_WIDTH // 2 # ボールの初期位置(横方向)
BALL_Y = PADDLE_Y - BALL_HEIGHT # ボールの初期位置(縦方向)

ball = pygame.Rect(BALL_X, BALL_Y, BALL_WIDTH, BALL_HEIGHT)
BALL_SPEED_X = 2 # ボールの速度(横方向)
BALL_SPEED_Y = -2 # ボールの速度(縦方向)

# ブロック
BLOCK_WIDTH = 40 # ブロックの幅
BLOCK_HEIGHT = 20 # ブロックの高さ
BLOCKS_PER_ROW = 10 # 1行に並べるブロックの数
BLOCK_ROWS = 5 # ブロックの行数

blocks = []
for i in range(BLOCK_ROWS):
    for j in range(BLOCKS_PER_ROW):
        block_x = j * BLOCK_WIDTH
        block_y = i * BLOCK_HEIGHT
        block = pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT)
        blocks.append(block)

# スコア
score = 0
font = pygame.font.Font(None, 30)

while True:
    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # キーボードの状態を取得
    keys = pygame.key.get_pressed()

    # パドルの移動
    if keys[K_LEFT] and paddle.left > 0:
        paddle.x -= 5
    if keys[K_RIGHT] and paddle.right < WINDOW_WIDTH:
        paddle.x += 5
    
    # ボールの移動
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # ボールの反射
    if ball.left < 0 or ball.right > WINDOW_WIDTH:
        BALL_SPEED_X = -BALL_SPEED_X
    if ball.top < 0:
        BALL_SPEED_Y = -BALL_SPEED_Y
    
    # ボールが画面下に落ちたら
    if ball.bottom > WINDOW_HEIGHT:
        game_over_surface = font.render("GameOver", True, (0, 0, 0))
        screen.blit(game_over_surface, (WINDOW_WIDTH//2-50, WINDOW_HEIGHT//2))
        pygame.display.update()
        # 3秒間待つ
        time.sleep(3)
        pygame.quit()
    
    # ブロックが全て消えたら
    if len(blocks) == 0:
        game_clear_surface = font.render("GameClear", True, (0, 0, 0))
        screen.blit(game_clear_surface, (WINDOW_WIDTH//2-50, WINDOW_HEIGHT//2))
        pygame.display.update()
        # 3秒間待つ
        time.sleep(3)
        pygame.quit()

    # ボールとパドルの衝突
    if ball.colliderect(paddle):
        BALL_SPEED_Y = -BALL_SPEED_Y

    # ボールとブロックの衝突
    for block in blocks:
        if ball.colliderect(block):
            blocks.remove(block) # ブロックを削除
            BALL_SPEED_Y = -BALL_SPEED_Y
            score += 10
    
    # ウインドウを白で塗りつぶす
    screen.fill((255, 255, 255))

    # パドルを描画
    pygame.draw.rect(screen, (0, 0, 0), paddle)
    # ボールを描画
    pygame.draw.ellipse(screen, (0, 0, 0), ball)

    # ブロックを描画
    for block in blocks:
        pygame.draw.rect(screen, (255, 0, 0), block)
    
    # スコアを描画
    score_surface = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    pygame.display.update()
    clock.tick(FPS)