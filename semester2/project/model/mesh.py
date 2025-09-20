# import numpy as np
import glm
from model.point_cloud import PointCloud


class Mesh(PointCloud):
    # points: list of 3d vectors
    # indices: list of polygons defined by point ids
    def __init__(
        self,
        points: list[glm.vec3],
        indices: list[list[int]]
    ):
        super().__init__(points)
        # self.indices = list[list[int]](indices)
        self.faces = list(indices)
