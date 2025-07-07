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
