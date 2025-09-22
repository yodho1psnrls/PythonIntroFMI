# import numpy as np
import glm
from model.point_cloud import PointCloud
from model.vertex import Vertex


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
        points: list[Vertex] = None,
        faces: list[list[int]] = None
    ):
        super().__init__(points)
        self.faces = list(faces) if faces else []
        # if not self.are_faces_valid():
        #     raise RuntimeError("one of the faces contains non-valid point index")

    # TODO:
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
        area = 0.0
        # The shoelace formula, but used in 3d,
        # We assume that same face points lie on the same plane !
        # And we assume all faces to have consistent ordering
        #  of their points, relative to the face surface normal
        # Wont error handle this, because we allow small deviations
        for face in self.faces:
            N = len(face)
            for i in range(N):
                p0 = self.points[face[i]]
                p1 = self.points[face[(i+1) % N]]
                area += glm.length(glm.cross(p0.pos, p1.pos))
        return abs(area)/2

    # polyhedron volume approximation
    # https://stackoverflow.com/questions/1406029/how-to-calculate-the-volume-of-a-3d-mesh-object-the-surface-of-which-is-made-up
    def volume(self):
        # you need to sum up all pyramids with
        # origin(0, 0, 0) as tip and the face as a base
        pass

    # collapses/combines same position points into a single one
    #  until all points have a unique position
    # This is useful in the case of the parametric sphere,
    #  where at the top and botoom there are multiple points
    #  condensed in the same position
    def collapse_points(self):
        pass

    def load(self, file_path: str):
        pass

    # https://en.wikipedia.org/wiki/Wavefront_.obj_file
    def save(self, file_path: str):
        if file_path[-4:] != '.obj':
            file_path += '.obj'
        with open(file_path, "w") as f:
            for p in self.points:
                f.write(f"v  {p.pos.x} {p.pos.y} {p.pos.z}\n")
            for p in self.points:
                f.write(f"vt {p.uv.x} {p.uv.y}\n")
            for p in self.points:
                f.write(f"vn {p.norm.x} {p.norm.y} {p.norm.z}\n")
            for face in self.faces:
                # ids = [i + 1 for i in face]
                ids = [f"{i+1}/{i+1}/{i+1}" for i in face]
                f.write("f " + " ".join(ids) + "\n")

    def update_normals(self):
        for p in self.points:
            p.norm = glm.vec3(0, 0, 0)
        for face in self.faces:
            N = len(face)
            for i in range(N):
                p0 = self.points[face[(i-1) % N]]
                p1 = self.points[face[i]]
                p2 = self.points[face[(i+1) % N]]
                p1.norm += glm.cross(p2.pos-p1.pos, p0.pos-p1.pos)
        for p in self.points:
            p.norm = glm.normalize(p.norm)

