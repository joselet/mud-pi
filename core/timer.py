import time

class Timer:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.last_time = time.time()

    def check_and_execute(self):
        current_time = time.time()
        if current_time - self.last_time >= self.interval:
            self.callback()
            self.last_time = current_time
