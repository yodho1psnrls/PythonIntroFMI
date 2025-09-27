from abc import ABC, abstractmethod
import numpy as np
import numexpr as ne
import model.util as u


# This gives a 3d vector with the derivatives of the sdf
'''
def gradient(p: np.array, eq, h=u.eps) -> np.array:
    if p.shape[0] != 3:
        raise RuntimeError("p should be a 3d vector")
    e = u.AXIS * h
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
'''


def gradient(points: np.array, eq, h=u.eps) -> np.array:
    e = u.AXIS * h
    # return [[
    #     eq(p+e[0]) - eq(p-e[0]),
    #     eq(p+e[1]) - eq(p-e[1]),
    #     eq(p+e[2]) - eq(p-e[2]),
    # ] for p in points]
    return np.stack((
        eq(points+e[0]) - eq(points-e[0]),
        eq(points+e[1]) - eq(points-e[1]),
        eq(points+e[2]) - eq(points-e[2]),
    ), axis=1) / (2.0 * h)


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


'''
class SDF:
    def __init__(self, eq: str):
        self.eq = eq

    def __str__(self):
        return self.eq

    def __or__(self, other):
        return SDF(f"max(({self}), ({other}))")

    def __and__(self, other):
        return SDF(f"max(({self}), ({other}))")

    def __call__(self, points):
        x, y, z = points[:, 0], points[:, 1], points[:, 2]
        local_dict = {"x": x, "y": y, "z": z}
        return ne.evaluate(self.expr, local_dict=local_dict)
'''


class Equation:
    def __init__(self, eq: str):
        # ne.validate(eq)  # raises an exception if not valid expression
        self.eq = eq

    def __call__(self, points: np.array) -> np.array:
        x, y, z = points[:, 0], points[:, 1], points[:, 2]
        local_dict = {"x": x, "y": y, "z": z}
        return ne.evaluate(self.eq, local_dict=local_dict)


# Serves like decorator for sdfs
class UnaryModifier(ABC):
    def __init__(self, eq: Equation):
        pass

    @abstractmethod
    def __call__(self, points: np.array) -> np.array:
        pass


# Combines two sdfs
class BinaryModifier(ABC):
    def __init__(self, lhs: Equation, rhs: Equation):
        pass

    @abstractmethod
    def __call__(self, points: np.array) -> np.array:
        pass


class Inflate(UnaryModifier):
    def __init__(self, eq: Equation, dist: float):
        self.eq
        self.dist = dist

    def __call__(self, points: np.array) -> np.array:
        return self.eq(points) + self.dist


# Extrusion
class Elongate(UnaryModifier):
    def __init__(self, eq: Equation, a: np.array, b: np.array):
        if not (a.shape == (3) and b.shape == (3)):
            raise ValueError("a and b should be 3d vectors")
        self.eq
        self.a = a
        self.b = b

    @np.vectorize
    def per_point(self, p: np.array) -> np.array:
        pa = p - self.a
        ba = self.b - self.a
        h = u.clamp(np.dot(pa, ba) / np.dot(ba, ba), 0.0, 1.0)
        return pa - ba*h

    def __call__(self, points: np.array) -> np.array:
        if not (len(points.shape) == 2 and points.shape[1] == 3):
            raise ValueError("the given points should be an array of 3d vectors")
        return self.eq(self.per_point(points))


class Revolution(UnaryModifier):
    def __init__(self, eq: Equation, r: float):
        self.eq
        self.r = r

    # def __call__(self, points: np.array) -> np.array:
    #     q = np.array([np.linalg.norm(np.array([p[0], p[2]])) - self.r0, p[1]])
    #     return np.linalg.norm(q) - self.r1

