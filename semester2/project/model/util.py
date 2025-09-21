import glm
# from sys import float_info
# very small positive number
# eps = float_info.epsilon

# eps = 1e-7
eps = 1e-5

AXIS = [
    glm.vec3(1, 0, 0),
    glm.vec3(0, 1, 0),
    glm.vec3(0, 0, 1),
]


def sign(x: float) -> int:
    return int(x / abs(x) if bool(x) else 1)
    # return x / abs(x) * bool(x) + not bool(x)
