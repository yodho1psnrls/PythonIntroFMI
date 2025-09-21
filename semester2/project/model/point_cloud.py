# import numpy as np
import glm


class Vertex:
    def __init__(self, pos=glm.vec3(), norm=glm.vec3(), uv=glm.vec2()):
        self.pos = pos
        self.norm = norm
        self.uv = uv


class PointCloud:
    # points: list of 3d vectors
    def __init__(
        self,
        points=list[Vertex](),
    ):
        # self.points = list(map(glm.vec3, points))
        # self.points = list(map(Vertex, points))
        self.points = list(points)

    # def __sum__()
