class TimeKeeper:
    def __init__(self):
        self._now_frame_time = 0 #ゲーム開始時からの時間
        self._reborn_frame_time = 0 #エネミーを復活させる周期
        
        self.generate_enemy_cycle = 1 #エネミーが復活する周期の管理
        self.enemy_bullet_cycle = 1 #エネミーが弾を打つ周期の管理

        self.now_second = 0
        self.reborn_second = 0
    
    def add_frame_time(self, frame_time):
        self._now_frame_time += frame_time
        self._reborn_frame_time += frame_time

        self.now_second = self._now_frame_time // 1000
        self.reborn_second = self._reborn_frame_time // 1000

    def add_enemy_bullet_cycle(self, cycle):
        self.enemy_bullet_cycle += cycle

    def add_generate_enemy_cycle(self, cycle):
        self.generate_enemy_cycle += cycle
    
    def reset_now_time(self):
        self._now_frame_time = 0
        self._now_second = 0

    def reset_reborn_time(self):
        self._reborn_frame_time = 0
        self._reborn_second = 0