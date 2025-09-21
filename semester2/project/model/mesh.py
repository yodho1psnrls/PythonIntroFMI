# import numpy as np
import glm
from model.point_cloud import PointCloud
from model.point_cloud import Vertex


# a polyhedron class
class Mesh(PointCloud):
    def is_valid_point(self, id: int) -> bool:
        return 0 <= id and id < len(self.points)

    def are_faces_valid(self) -> bool:
        for face in self.faces:
            if len(face) < 3:
                return False
            for i in face:
                if not self.is_valid_point(i):
                    return False
        return True

    # points: list of 3d vectors
    # indices: list of polygons defined by point ids
    def __init__(
        self,
        points=list[Vertex](),
        faces=list[list[int]]()
    ):
        super().__init__(points)
        self.faces = list(faces)
        # if not self.are_faces_valid():
        #     raise RuntimeError("one of the faces contains non-valid point index")

    # recursively split the polygons by their smallest
    #  diagonal, untill all polygon faces are triangles
    def triangulate(self):
        pass

    def are_faces_nsided(self, n):
        for face in self.faces:
            if not len(face) == n:
                return False
        return True

    def is_triangulated(self):
        return self.are_faces_nsided(3)

    # def face_points(self, face_id):
    #     return [self.points[i] for i in self.faces[face_id]]

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
