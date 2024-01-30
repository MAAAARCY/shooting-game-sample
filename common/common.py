from .window.size import WindowSize
from .window.fps import WindowFPS

class Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class Common(Singleton):
    def __init__(self):
        self.window_size = WindowSize()
        self.window_fps = WindowFPS()
    def get_window_size(self):
        return self.window_size
    def get_fps(self):
        return self.window_fps.FPS