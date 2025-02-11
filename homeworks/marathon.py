def seconds_to_time(seconds)

class Time:
    def __init__(self, h: int, m: int, s: int):
        self.h = h
        self.m = m
        self.s = s

    def __init__(self, seconds: int):
        self.h = seconds / 360
        self.m = (seconds / 60) % 360
        self.s = seconds % 60

    def flat_time(self) -> int:
        return self.s + self.m*60 + self.h * 60 * 60

    def time(seconds: int):
        return Time(seconds / 360, (seconds/60) % 360, seconds % 60)

    def diff(self, other):
        return time(self.flat_time() - flat_time(other))
