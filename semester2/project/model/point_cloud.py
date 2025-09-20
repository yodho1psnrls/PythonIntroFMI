# import numpy as np
import glm


class PointCloud:
    # points: list of 3d vectors
    def __init__(
        self,
        points: list[glm.vec3],
    ):
        self.points = list(map(glm.vec3, points))
