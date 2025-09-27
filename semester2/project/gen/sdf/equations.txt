import numpy as np
from math import sqrt
from math import sin
from math import cos
from math import exp
from math import pi
from model.util import eps
from model.util import AXIS
from model.util import clamp


def test_eq(p: np.array) -> float:
    return np.linalg.norm(p) - 0.75


# This gives a 3d vector with the derivatives of the sdf
def gradient(p: np.array, eq, h=eps) -> np.array:
    if p.shape[0] != 3:
        raise RuntimeError("p should be a 3d vector")
    e = AXIS * h
    # Forward differentiation (Faster, and precise enough with small eps)
    # p_val = eq(p)
    # return glm.vec3(
    #     eq(p+ex) - p_val,
    #     eq(p+ey) - p_val,
    #     eq(p+ez) - p_val,
    # ) / h
    # Central differentiation (More accurate, even with bigger eps values)
    return np.array([
        eq(p+e[0]) - eq(p-e[0]),
        eq(p+e[1]) - eq(p-e[1]),
        eq(p+e[2]) - eq(p-e[2]),
    ]) / (2.0*h)


# Below are a bunch of SDFs(Signed Distance Functions) which
#  given a 3d point, return the closest distance to the surface of a volume
#  distance < 0 means that the point is inside the volume or behind the surface
#  distance == 0 means that the point is exactly on the surface of the volume
#  distance > 0 means that the point is outside the volume or above the surface

# References:
# https://en.wikipedia.org/wiki/Signed_distance_function
# https://iquilezles.org/articles/distfunctions/
# https://www.shadertoy.com/

# https://iquilezles.org/articles/smin/
# def smin(a: float, b: float, k: float = 0.1):
#     k *= 1.0
#     r = glm.exp2(-a/k) + glm.exp2(-b/k)
#     return -k*glm.log2(r)


# The simplest SDF is of a sphere, it essentially
#  gives you the distance from the given point p
#  to the center of the sphere, minus its radius
class Sphere:
    def __init__(self, radius=1.0):
        self.r = radius

    def __call__(self, p: np.array) -> float:
        if p.shape[0] != 3:
            raise RuntimeError("p should be a 3d vector")
        return np.linalg.norm(p) - self.r


# Torus | Donut Shape
class Torus:
    def __init__(self, major_radius: float, minor_radius: float):
        self.r0 = major_radius
        self.r1 = minor_radius

    def __call__(self, p: np.array) -> float:
        if p.shape[0] != 3:
            raise RuntimeError("p should be a 3d vector")
        # q = np.array([np.linalg.norm(p.xz) - self.r0, p.y])
        q = np.array([np.linalg.norm(np.array([p[0], p[2]])) - self.r0, p[1]])
        return np.linalg.norm(q) - self.r1


def polynomial_degree3(p: np.array) -> float:
    x, y, z = p[0], p[1], p[2]
    return (1-3*x-3*y-3*z)*(x*y+x*z+y*z)+6*x*y*z


class Capsule:
    def __init__(self, a: np.array, b: np.array, r: float):
        self.a = np.array(a, dtype=np.float32)
        self.b = np.array(b, dtype=np.float32)
        self.r = r

    def __call__(self, p: np.array):
        pa = p - self.a
        ba = self.b - self.a;
        h = clamp(np.dot(pa, ba) / np.dot(ba, ba), 0.0, 1.0)
        return np.linalg.norm(pa - ba*h) - self.r


# def pumpkin(p: np.array) -> float:
#     ss = Sphere(0.5)
#     diff = np.array([0.5, 0, 0])
#     return smin(ss(p-diff), ss(p+diff), 0.1)
#     # return min(ss(p-diff), ss(p+diff))
