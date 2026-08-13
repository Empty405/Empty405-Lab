import time


class RateLimiter:
    def __init__(self, max_requests=5, window_seconds=10):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []

    def allow(self):
        now = time.time()

        self.requests = [
            t for t in self.requests
            if now - t < self.window_seconds
        ]

        if len(self.requests) >= self.max_requests:
            return False

        self.requests.append(now)
        return True
