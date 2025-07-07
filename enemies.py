# File: enemies.py

class PrisonGuard():
    def __init__(self, init_x, init_y, init_direction, \
        move_l, move_r, vis_l, vis_r):
        self.MAX_FRAME_DELAY = 5
        self.x = init_x
        self.y = init_y
        self.direction = init_direction
        self.l_bound = move_l
        self.r_bound = move_r
        self.l_sight = vis_l
        self.r_sight = vis_r
        self.animation = 0
        if init_direction < 0:
            self.animation = 1
        self.anim_frame = 0
        self.frame_delay = self.MAX_FRAME_DELAY
