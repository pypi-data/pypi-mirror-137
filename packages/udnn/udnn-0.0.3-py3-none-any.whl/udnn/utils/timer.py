from __future__ import absolute_import
import time


class Timer(object):
    stat_name = 'time'

    def __init__(self):
        super(Timer, self).__init__()
        self.last_time = time.time()

    def get_value(self):
        if self.last_time:
            now = time.time()
            duration = now - self.last_time
            return duration
        else:
            self.last_time = time.time()
            return
