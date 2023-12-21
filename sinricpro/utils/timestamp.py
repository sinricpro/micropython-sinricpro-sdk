import utime

class Timestamp:
    def __init__(self):
        self.timestamp_ms = 0  # Store timestamp in milliseconds
        self.last_update = utime.ticks_ms()

    def get_timestamp(self):
        self.update()
        return self.timestamp_ms // 1000  # Integer division for seconds

    def set_timestamp(self, new_timestamp):
        self.timestamp_ms = new_timestamp * 1000
        self.last_update = utime.ticks_ms()

    def update(self):
        if not self.timestamp_ms:
            return
        current_millis = utime.ticks_ms()
        diff_millis = current_millis - self.last_update
        self.timestamp_ms += diff_millis
        self.last_update = current_millis
