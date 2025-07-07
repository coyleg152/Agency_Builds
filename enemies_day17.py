# File: enemies_day17.py

class PrisonGuard():
    def __init__(self, init_x, init_y, init_direction, init_l, init_r):
        self.MAX_FRAME_DELAY = 5
        self.x = init_x
        self.y = init_y
        self.direction = init_direction
        self.l_bound = init_l
        self.r_bound = init_r
        self.animation = 0
        if init_direction < 0:
            self.animation = 1
        self.anim_frame = 0
        self.frame_delay = self.MAX_FRAME_DELAY
