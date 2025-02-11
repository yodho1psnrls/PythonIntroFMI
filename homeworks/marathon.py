from random import random as rand


def get_time(seconds):
    seconds = int(seconds)
    return Time(seconds // 3600, (seconds // 60) % 60, seconds % 60)


class Time:
    def __init__(self, h: int, m: int, s: int):
        self.h = h
        self.m = m
        self.s = s

    def flat(self) -> int:
        return self.s + self.m * 60 + self.h * 3600

    def diff(self, other):
        return get_time(self.flat() - other.flat())

    def __str__(self):
        # return str(self.h) + ":" + str(self.m) + ":" + str(self.s)
        return f"{self.h:02}:{self.m:02}:{self.s:02}"


class Competitor:
    def __init__(self,
                 number: int,
                 name: str,
                 family: str,
                 start: Time,
                 end: Time):
        self.number = number
        self.name = name
        self.family = family
        self.start = start
        self.end = end

    def time_running(self) -> Time:
        return self.end.diff(self.start)

    def seconds_running(self) -> Time:
        return self.end.flat() - self.start.flat()

    def __str__(self):
        return str(self.end.diff(self.start))


if __name__ == "__main__":
    # print(str(get_time(Time(13, 31, 27).flat())))

    runners = [Competitor] * 10

    for i in range(10):
        start = i * 5 * 60  # in seconds
        end = start + rand() * (3 * 3600) + 4 * 3600  # in seconds

        start = get_time(start)  # in Time
        end = get_time(end)  # in Time

        runners[i] = Competitor(i, "Jeko", "Jekov", start, end)

    runners = sorted(runners, key=lambda runner: runner.seconds_running())

    for runner in runners:
        print(runner)


#
