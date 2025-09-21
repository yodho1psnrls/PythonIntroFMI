# import numpy as np
import glm
from model.point_cloud import PointCloud


# a polyhedron class
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

    # recursively split the polygons by their smallest
    #  diagonal, untill all polygon faces are triangles
    def triangulate(self):
        pass

    # the area of the polyhedron
    def area(self):
        pass

    # polyhedron volume approximation
    def volume(self):
        pass

    # collapses/combines same position points into a single one
    #  until all points have a unique position
    # This is useful in the case of the parametric sphere,
    #  where at the top and botoom there are multiple points
    #  condensed in the same position
    def collapse_points(self):
        pass
