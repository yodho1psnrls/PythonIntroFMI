# import numpy as np
import glm
from math import sqrt
from math import sin
from math import cos
from math import exp
from math import pi
from model.util import eps
# from model.util import AXIS


# This gives a 3d vector with the derivatives of the sdf
def gradient(p: glm.vec3, eq, h=eps) -> glm.vec3:
    ex = glm.vec3(h, 0.0, 0.0)
    ey = glm.vec3(0.0, h, 0.0)
    ez = glm.vec3(0.0, 0.0, h)
    # Forward differentiation (Faster, and precise enough with small eps)
    # p_val = eq(p)
    # return glm.vec3(
    #     eq(p+ex) - p_val,
    #     eq(p+ey) - p_val,
    #     eq(p+ez) - p_val,
    # ) / eps
    # Central differentiation (More accurate, even with bigger eps values)
    return glm.vec3(
        eq(p+ex) - eq(p-ex),
        eq(p+ey) - eq(p-ey),
        eq(p+ez) - eq(p-ez),
    ) / (2.0*eps)


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
def smin(a: float, b: float, k: float = 0.1):
    k *= 1.0
    r = glm.exp2(-a/k) + glm.exp2(-b/k)
    return -k*glm.log2(r)


# The simplest SDF is of a sphere, it essentially
#  gives you the distance from the given point p
#  to the center of the sphere, minus its radius
class Sphere:
    def __init__(self, radius=1.0):
        self.r = radius

    def __call__(self, p: glm.vec3) -> float:
        return sqrt(p.x*p.x+p.y*p.y+p.z*p.z) - self.r
    # return glm.length(p) - self.r


# Torus | Donut Shape
class Torus:
    def __init__(self, major_radius: float, minor_radius: float):
        self.r0 = major_radius
        self.r1 = minor_radius

    def __call__(self, p: glm.vec3) -> float:
        q = glm.vec2(glm.length(p.xz) - self.r0, p.y)
        return glm.length(q) - self.r1


def pumpkin(p: glm.vec3) -> float:
    ss = Sphere(0.5)
    diff = glm.vec3(0.5, 0, 0)
    return smin(ss(p-diff), ss(p+diff), 0.1)
    # return min(ss(p-diff), ss(p+diff))
