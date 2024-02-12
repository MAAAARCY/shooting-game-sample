from .window.size import WindowSize
from .window.fps import WindowFPS

from .time.time_keeper import TimeKeeper


class Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class Common(Singleton):
    def __init__(self):
        self.window_size = WindowSize()
        self.window_fps = WindowFPS()
        self.time_keeper = TimeKeeper()

    def get_window_size(self):
        return self.window_size

    def get_fps(self):
        return self.window_fps.FPS

    def get_time_keeper(self, generate_enemy_cycle, enemy_bullet_cycle, boss_bullet_cycle):
        self.time_keeper = TimeKeeper(
            generate_enemy_cycle, enemy_bullet_cycle, boss_bullet_cycle)
        return self.time_keeper
