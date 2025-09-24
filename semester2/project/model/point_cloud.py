import numpy as np

vertex_dtype = np.dtype([
    ("pos", "f4", 3),   # 3D position
    ("norm", "f4", 3),  # 3D surface normal
    ("uv", "f4", 2)     # 2D uv texture coordinates
])


class PointCloud:
    def __init__(
        self,
        points: np.array = None,    # np.ndarray[vertex_dtype]
    ):
        if points is None:
            self.points = np.array([], dtype=vertex_dtype)
        else:
            self.points = np.array(points, dtype=vertex_dtype)
        if len(self.points.shape) != 1:
            raise RuntimeError("The points should be a vector of vertex_dtype")

    def __sizeof__(self) -> int:
        return len(self.points)

    def __iter__(self):
        return iter(self.points)

    @property
    def positions(self) -> np.array:
        return self.points['pos']

    @positions.setter
    def positions(self, value: np.array):
        # optional: you could add validation
        if value.shape != self.points["pos"].shape:
            raise ValueError("Shape mismatch")
        self.points["pos"][:] = value

    @property
    def normals(self) -> np.array:
        return self.points['norm']

    @normals.setter
    def normals(self, value: np.array):
        # optional: you could add validation
        if value.shape != self.points["norm"].shape:
            raise ValueError("Shape mismatch")
        self.points["norm"][:] = value

    @property
    def uvs(self) -> np.array:
        return self.points['uv']

    @uvs.setter
    def uvs(self, value: np.array):
        # optional: you could add validation
        if value.shape != self.points["uv"].shape:
            raise ValueError("Shape mismatch")
        self.points["uv"][:] = value
