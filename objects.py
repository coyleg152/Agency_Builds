# File: objects.py

class SpikeTrap():
    def __init__(self, _x, _y, _l, _h, init_state, _max, init_delay):
        self.x = _x
        self.y = _y
        self.length = _l
        self.height = _h
        self.state = init_state
        self.max_delay = _max
        self.delay = init_delay

class Checkpoint():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.length = 0
        self.height = 0
        self.visible = False
        self.activated = False
        self.level = "X"
