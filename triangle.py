import math

def is_triangle(a: float, b: float, c: float) -> bool:
    biggest = max(a, b, c)
    return biggest < a + b + c - biggest


def area(a: float, b: float, c: float) -> float:
    p = 0.5 * (a + b + c)
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


if __name__ == "__main__":
    print("blqblq")

