import utime

class RateLimiter:
    def __init__(self, initial_rate):
        self.events_per_minute = initial_rate
        self.burst_size = 5
        self.decay_rates = {60: 30, 30: 5}
        self.interval = 60 / initial_rate
        self.last_event_time = 0
        self.remaining_tokens = 5

    def try_acquire(self):
        current_time = utime.time()
        elapsed_time = current_time - self.last_event_time

        if elapsed_time >= self.interval:
            self.remaining_tokens = min(self.burst_size, self.remaining_tokens + int(elapsed_time / self.interval))
            self.last_event_time = current_time

        if self.remaining_tokens > 0:
            self.remaining_tokens -= 1
            return True
        else:
            self.adjust_rate()
            return False

    def adjust_rate(self):
        if self.events_per_minute in self.decay_rates:
            self.events_per_minute = self.decay_rates[self.events_per_minute]
            self.interval = 60 / self.events_per_minute
            self.remaining_tokens = self.burst_size

# Example usage
# initial_rate = 60
# burst_size = 5
# decay_rates = {60: 30, 30: 5}

# limiter = RateLimiter(initial_rate, burst_size, decay_rates)
