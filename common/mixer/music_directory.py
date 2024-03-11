import pygame
from pygame.locals import *

from dotenv import load_dotenv
import os
load_dotenv()


class MusicDirectory:
    def __init__(self):
        self._game_bgm = "music/{}".format(os.getenv('GAME_BGM'))
        self._shot_sound = "music/{}".format(os.getenv('SHOT_SOUND'))
        self._special_shot_sound = "music/{}".format(os.getenv('SPECIAL_SHOT_SOUND'))
        self._hit_sound = "music/{}".format(os.getenv('HIT_SOUND'))

    def start_bgm(self):
        pygame.mixer.music.load(self._game_bgm)
        pygame.mixer.music.play(-1)

    def pause_bgm(self):
        pygame.mixer.music.pause()

    def unpause_bgm(self):
        pygame.mixer.music.unpause()

    def stop_bgm(self):
        pygame.mixer.music.stop()

    def shot_sound_play(self):
        pygame.mixer.Sound(self._shot_sound).play()

    def special_shot_sound_play(self):
        pygame.mixer.Sound(self._special_shot_sound).play()

    def hit_sound_play(self):
        pygame.mixer.Sound(self._hit_sound).play()
