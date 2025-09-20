import numpy as np
from math import sin
from math import cos
from math import exp
from math import pi


def sphere(uv: np.array) -> np.array:
    u = 2 * pi * uv[0]
    v = 2 * pi * uv[1]
    return np.array([
        sin(u)*cos(v),
        sin(u)*sin(v),
        cos(u),
    ])


def cone(uv: np.array) -> np.array:
    u = 2 * pi * uv[0]
    v = uv[1]
    return np.array([
        (1.0 - v) * cos(u),
        (1.0 - v) * sin(u),
        v
    ])


# https://math.libretexts.org/Bookshelves/Calculus/Supplemental_Modules_(Calculus)/Vector_Calculus/2%3A_Vector-Valued_Functions_and_Motion_in_Space/2.7%3A_Parametric_Surfaces
def fold_paper(uv: np.array) -> np.array:
    u = 2 * pi * uv[0]
    v = 2 * pi * uv[1]
    return np.array([
        sin(u),
        cos(v),
        exp(2*u**(1/3) + 2*v**(1/3))
    ])


def hour_glass(uv: np.array) -> np.array:
    u = 2.0 * pi * uv[0]
    v = 2.0 * pi * uv[1]
    return np.array([
        cos(u)*cos(v),
        cos(u)*sin(v),
        uv[0],  # u
    ])


def screw(uv: np.array) -> np.array:
    u = 2.0 * pi * uv[0]
    v = 2.0 * pi * uv[1]
    return np.array([
        cos(u)*cos(v),
        cos(u)*sin(v),
        uv[1],  # v
    ])

# ----------------------------------------------------------------- #

# https://www.reddit.com/r/threejs/comments/1jb12bm/a_gallery_of_parametric_surfaces_with_their/


