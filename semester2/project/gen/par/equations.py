import numpy as np
# import glm
from math import sin
from math import cos
from math import exp
from math import pi
from model.util import eps
import numexpr as ne


# Derivative of a parametric equation with respect to u
def tangent(uv: np.array, eq, h=eps) -> np.array:
    # Forward differentiation (Precise enough with small eps):
    # return (eq(uv + glm.vec2(eps, 0.0)) - eq(uv)) / eps
    # Central differentiation (More accurate):
    a = uv + (h, 0.0)
    b = uv - (h, 0.0)
    return (eq(a) - eq(b)) / (2.0*h)


# Derivative of a parametric equation with respect to v
def bitangent(uv: np.array, eq, h=eps) -> np.array:
    # Forward differentiation (Precise enough with small eps):
    # return (eq(uv + glm.vec2(0.0, eps)) - eq(uv)) / eps
    # Central differentiation (More accurate):
    a = uv + (0.0, h)
    b = uv - (0.0, h)
    return (eq(a) - eq(b)) / (2.0*h)


# The cross product of the dirivatives of the parametric
#  equation with respect to u and v (points outwards from the surface)
def gradient(uv: np.array, eq, h=eps) -> np.array:
    return np.linalg.cross(tangent(uv, eq, h), bitangent(uv, eq, h))


class PAR:
    def __init__(self, eq: str):
        eqs = eq.split(',')
        if len(eqs) != 3:
            raise ValueError("Three equations separated by comma are needed for a parametric function")
        self.eqx, self.eqy, self.eqz = eqs

    # def __init__(self, eqx: str, eqy: str, eqz: str):
    #     self.eqx = eqx
    #     self.eqy = eqy
    #     self.eqz = eqz

    def evaluate(self, u, v):
        u = np.array(u, dtype=np.float32)
        v = np.array(v, dtype=np.float32)
        local_dict = {"u": u, "v": v}

        x = ne.evaluate(self.eqx, local_dict=local_dict)
        y = ne.evaluate(self.eqy, local_dict=local_dict)
        z = ne.evaluate(self.eqz, local_dict=local_dict)

        return np.stack((x, y, z), axis=-1)


def sphere(uv: np.array):
    u = 2 * pi * (1.0-uv[0])
    v = 1 * pi * uv[1]
    return np.array([
        cos(u)*sin(v),
        sin(u)*sin(v),
        cos(v),
    ])


def cone(uv: np.array):
    u = 2 * pi * uv[0]
    v = uv[1]
    return np.array([
        (1.0 - v) * cos(u),
        (1.0 - v) * sin(u),
        v * 2.0 - 1.0,
    ])


# https://math.libretexts.org/Bookshelves/Calculus/Supplemental_Modules_(Calculus)/Vector_Calculus/2%3A_Vector-Valued_Functions_and_Motion_in_Space/2.7%3A_Parametric_Surfaces
def fold_paper(uv: np.array):
    u = 2 * pi * uv[0]
    v = 2 * pi * uv[1]
    return np.array([
        sin(u),
        cos(v),
        exp(2*u**(1/3) + 2*v**(1/3))
    ])


def hour_glass(uv: np.array):
    u = 2.0 * pi * uv[0]
    v = 2.0 * pi * uv[1]
    return np.array([
        cos(u)*cos(v),
        cos(u)*sin(v),
        uv[0],  # u
    ])


def screw(uv: np.array):
    u = 2.0 * pi * uv[0]
    v = 2.0 * pi * uv[1]
    return np.array([
        cos(u)*cos(v),
        cos(u)*sin(v),
        uv[1],  # v
    ])

# ----------------------------------------------------------------- #

# https://www.reddit.com/r/threejs/comments/1jb12bm/a_gallery_of_parametric_surfaces_with_their/


