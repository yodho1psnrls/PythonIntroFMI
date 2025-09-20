class Foo:
    def __init__(self, x):
        self.x = x

    def calc(self, y):
        return self.x + y

    def __call__(self, y):
        return self.x + y


def for_each(func, vals: list):
    return [func(x) for x in vals]


if __name__ == '__main__':
    f = Foo(15)
    vals = [0, 1, 2, 3, 4]
    # print(for_each(f.calc, vals))
    print(for_each(f, vals))
