class TimeKeeper:
    def __init__(self, generate_enemy_cycle=1, enemy_bullet_cycle=1, boss_bullet_cycle=1, drop_item_cycle=5):
        self._now_frame_time = 0  # ゲーム開始時からの時間
        self._reborn_frame_time = 0  # エネミーを復活させる周期

        self.generate_enemy_cycle = generate_enemy_cycle  # エネミーが復活する周期の管理
        self.enemy_bullet_cycle = enemy_bullet_cycle  # エネミーが弾を打つ周期の管理
        self.boss_bullet_cycle = boss_bullet_cycle
        self.drop_item_cycle = drop_item_cycle

        self.now_second = 0
        self.reborn_second = 0

        self.now_milli_second = 0

    def add_frame_time(self, frame_time):
        self._now_frame_time += frame_time
        self._reborn_frame_time += frame_time

        self.now_second = self._now_frame_time // 1000
        self.reborn_second = self._reborn_frame_time // 1000

        self.now_milli_second = round(self._now_frame_time/1000, 1)

    def add_enemy_bullet_cycle(self, cycle):
        self.enemy_bullet_cycle += cycle

    def add_boss_bullet_cycle(self, cycle):
        self.boss_bullet_cycle += cycle

    def add_generate_enemy_cycle(self, cycle):
        self.generate_enemy_cycle += cycle

    def add_drop_item_cycle(self, cycle):
        self.drop_item_cycle += cycle

    def reset_now_time(self):
        self._now_frame_time = 0
        self._now_second = 0

    def reset_reborn_time(self):
        self._reborn_frame_time = 0
        self._reborn_second = 0
