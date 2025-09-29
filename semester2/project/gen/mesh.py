import numpy as np
from gen.point_cloud import PointCloud
from gen.point_cloud import vertex_dtype
from gen.util import timeit


# len(list(polygon_diagonals(n))) == n*(n-3)/2
def polygon_diagonals(n: int):
    # same as the modulo operator, but instead of giving
    # values from 0 to n-1, it gives from 1 to n
    # def up_mod(i: int) -> int:
    #     i = i % n
    #     i += n * (i == 0)
    #     return i

    for i in range(0, n-2):
        # for j in range(i+2, n+i-1):
        # for j in range(i+2, imin(n, n+i-1)):
        for j in range(i+2, n-(i == 0)):
            yield (i, j)


# a polyhedron class
class Mesh(PointCloud):
    def is_valid_point(self, id: int) -> bool:
        return 0 <= id and id < len(self.positions)

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
        points: np.array = None,
        faces: np.array = None
    ):
        super().__init__(points)
        if faces is not None:
            self.faces = np.array(faces, dtype=np.int32)
        else:
            self.faces = np.array([], dtype=np.int32)
        if len(self.faces.shape) != 2:
            raise RuntimeError("the faces should be a matrix of integers")
        if not self.are_faces_valid():
            raise RuntimeError("one of the faces contains non-valid point index")

    def __sizeof__(self) -> int:
        return len(self.faces)

    def __iter__(self):
        for face in self.faces:
            return self.points[face]

    def are_faces_nsided(self, n: int) -> bool:
        return self.faces.shape[1] == n

    def is_triangulated(self) -> bool:
        return self.are_faces_nsided(3)

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
                p0 = self.positions[face[i]]
                p1 = self.positions[face[(i+1) % N]]
                area += np.linalg.norm(np.linalg.cross(p0, p1))
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
            for p in self.positions:
                f.write(f"v  {p[0]} {p[1]} {p[2]}\n")
            for p in self.uvs:
                f.write(f"vt {p[0]} {p[1]}\n")
            for p in self.normals:
                f.write(f"vn {p[0]} {p[1]} {p[2]}\n")
            for face in self.faces:
                # ids = [i + 1 for i in face]
                ids = [f"{i+1}/{i+1}/{i+1}" for i in face]
                f.write("f " + " ".join(ids) + "\n")

    def update_normals(self):
        for n in self.normals:
            n = (0, 0, 0)
        for face in self.faces:
            p0 = self.positions[face[0]]
            p1 = self.positions[face[1]]
            p2 = self.positions[face[2]]
            n = np.linalg.cross(p2-p1, p0-p1)
            for i in face:
                self.normals[i] += n
        for n in self.normals:
            n /= np.linalg.norm(n)

    # TODO: recursively split the polygons by their smallest
    #  diagonal, untill all polygon faces are triangles
    # def triangulate(self):
    #     pass

    # Trims/Removes all points which are not used in any of the faces
    #  (also remaps the indices in the faces to the new point ids)
    def trim(self):
        old_to_new_id = dict()
        for face in self.faces:
            for i in range(len(face)):
                if face[i] in old_to_new_id:
                    face[i] = old_to_new_id[face[i]]
                else:
                    new_i = len(old_to_new_id)
                    old_to_new_id[face[i]] = new_i
                    face[i] = new_i
        new_points = np.zeros((len(old_to_new_id)), dtype=vertex_dtype)
        for old_i, new_i in old_to_new_id.items():
            new_points[new_i] = self.points[old_i]
        self.points = new_points

    '''
    def trim(self):
        old_to_new_id = np.full((len(self.points)), -1)
        found_points = 0
        for face in self.faces:
            for i in range(len(face)):
                if old_to_new_id[face[i]] != -1:
                    face[i] = old_to_new_id[face[i]]
                else:
                    new_i = found_points
                    old_to_new_id[face[i]] = new_i
                    face[i] = new_i
                    found_points += 1
        new_points = np.zeros((found_points), dtype=vertex_dtype)
        survived_points = self.points[]
        # for old_i, new_i in old_to_new_id.items():
        #     new_points[new_i] = self.points[old_i]
        self.points = new_points
    '''

    # Fast fan-like triangulation (Preserves consistent face order)
    def triangulate(self):
        if self.is_triangulated():
            return
        num_faces = self.faces.shape[0]
        tri_per_face = self.faces.shape[1] - 2
        triangles = np.zeros((num_faces * tri_per_face, 3), dtype=np.int32)
        for fi in range(len(self.faces)):
            face = self.faces[fi]
            for i in range(0, tri_per_face):
                triangles[fi*tri_per_face+i] = ([face[0], face[i+1], face[i+2]])
        self.faces = triangles

    def invert(self):
        for f in self.faces:
            f = f[::-1]
        for n in self.normals:
            n *= -1.0
