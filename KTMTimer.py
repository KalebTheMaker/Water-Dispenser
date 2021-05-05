from threading import Timer
import time

class KTMTimer(object):
    def __init__(self, interval, function, args=[], kwargs={}):
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self.start_time = 0

    def start(self):
        t = Timer(self._interval, self._function, *self._args, **self._kwargs)
        t.start()
        self.start_time = time.time()

    def elapsed(self):
        return time.time() - self.start_time

    def remaining(self):
        return self._interval - self.elapsed()