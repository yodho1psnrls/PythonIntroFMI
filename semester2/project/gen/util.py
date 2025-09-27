from numbers import Number
import numpy as np
# from sys import float_info
# very small positive number
# eps = float_info.epsilon
from functools import wraps
import time

# eps = 1e-7
eps = 1e-5

AXIS = np.array([
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
], dtype=np.int32)


# Linear Interpolation
def lerp(a, b, t):
    return a + (b - a) * t


# integer min (branchless)
def imin(a, b):
    COND = a < b
    return COND * a + (not COND) * b
    # result = a
    # result += (not a < b) * (b - a)
    # return result


def sign(x: float) -> int:
    return int(x / abs(x) if bool(x) else 1)
    # return x / abs(x) * bool(x) + not bool(x)


def clamp(x: float, a: float, b: float) -> float:
    if x < a:
        return a
    elif x > b:
        return b
    return x


def rotate(axis: np.array, angle: float):
    axis = np.array(axis, dtype=np.float32)
    axis = axis / np.linalg.norm(axis)
    c = np.cos(angle)
    s = np.sin(angle)
    t = 1 - c
    x, y, z = axis
    # Rodrigues' rotation formula
    return np.array([
        [t*x*x + c,     t*x*y - s*z, t*x*z + s*y],
        [t*x*y + s*z,   t*y*y + c,   t*y*z - s*x],
        [t*x*z - s*y,   t*y*z + s*x, t*z*z + c]
    ], dtype=np.float32)


def orientate(prev_forward, new_forward):
    pf = np.array(prev_forward, dtype=np.float32)
    nf = np.array(new_forward, dtype=np.float32)
    pf /= np.linalg.norm(pf)
    nf /= np.linalg.norm(nf)
    axis = np.cross(nf, pf)
    # return rotate(
    #     axis,
    #     # np.atan2(np.linalg.norm(axis), np.dot(nf, pf))
    #     np.acos(np.dot(pf, nf))
    # )
    c = np.dot(pf, nf)
    s = np.linalg.norm(axis)
    t = 1 - c
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    # Rodrigues' rotation formula
    return np.array([
        [t*x*x + c,     t*x*y - s*z, t*x*z + s*y],
        [t*x*y + s*z,   t*y*y + c,   t*y*z - s*x],
        [t*x*z - s*y,   t*y*z + s*x, t*z*z + c]
    ], dtype=np.float32)


# given a direction and up 3d vectors
# returns a 3x3 matrix which rotates from (1, 0, 0) to dir
def look_at(dir, up=np.array([0.0, 0.0, 1.0])):
    forward = dir
    forward /= np.linalg.norm(forward)       # forward
    right = np.cross(up, forward)
    right /= np.linalg.norm(right)
    new_up = np.cross(forward, right)
    # return np.matrix(np.vstack([right, new_up, forward]))
    return np.vstack([right, new_up, forward])


'''
# given a direction and up 3d vectors
# returns a 3x3 matrix which rotates from (1, 0, 0) to dir
def look_at(target, eye=np.array([0.0, 0.0, 0.0]), up=np.array([0.0, 0.0, 1.0])):
    forward = target-eye
    forward /= np.linalg.norm(forward)       # forward
    right = np.cross(up, forward)
    right /= np.linalg.norm(right)
    new_up = np.cross(forward, right)
    # return np.matrix(np.vstack([right, new_up, forward]))
    # return np.vstack([right, new_up, forward])
    return np.array([
        (right[0], new_up[0], forward[0], eye[0]),
        (right[1], new_up[1], forward[1], eye[1]),
        (right[2], new_up[2], forward[2], eye[2]),
        (0, 0, 0, 1),
    ])
'''


# https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f'Function {func.__name__}{args} {kwargs} took {total_time:.4f}s')
        print(f'{func.__name__} took {total_time:.4f}s')
        return result
    return timeit_wrapper

