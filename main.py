import pygame
from pygame.locals import *
import sys

from common.common import Common

from scenes.shooting_scene_1 import Shooting_scene_1

pygame.init()
clock = pygame.time.Clock()

fps = Common().get_fps()
window_size = Common().get_window_size()

screen = pygame.display.set_mode((window_size.width, window_size.height))
pygame.display.set_caption('シューティングゲーム')

while True:
    Shooting_scene_1().scene(screen, clock, fps)
