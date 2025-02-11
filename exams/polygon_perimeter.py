import math


def norm(vec):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])


def diff(a, b):
    return (a[0] - b[0], a[1] - b[1])


if __name__ == "__main__":
    perimeter = 0
    pos0 = None

    while True:
        input_line = input()
        if len(input_line) == 0:
            break

        pos1 = tuple(map(float, (input_line.split(", "))))
        if not pos0:
            pos0 = pos1
            continue
        else:
            perimeter += norm(diff(pos0, pos1))

    print(perimeter)
