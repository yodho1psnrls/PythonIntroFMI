import numpy as np
import numexpr as ne
from gen.util import timeit


class IsoField:
    def __init__(self, dim: list[int], min_pos=[-1, -1, -1], max_pos=[1, 1, 1]):
        self.dim = np.array(dim, dtype=np.int32)
        self.min_pos = np.array(min_pos, dtype=np.float32)
        self.max_pos = np.array(max_pos, dtype=np.float32)
        self.reset()

    def reset(self):
        num_points = np.prod(self.dim+np.ones((len(self.dim)), dtype=np.int32))
        # we will use the 4th coordinate to cache the sdf value
        self.points = np.zeros((num_points, 4), dtype=np.float32)
        for i in range(self.dim[0] + 1):
            for j in range(self.dim[1] + 1):
                for k in range(self.dim[2] + 1):
                    flat_id = self.flat_point_id(np.array([i, j, k]))
                    scale = self.max_pos - self.min_pos
                    offset = self.min_pos
                    self.points[flat_id][:-1] = np.array([
                        i/self.dim[0],
                        j/self.dim[1],
                        k/self.dim[2],
                    ]) * scale + offset

    # def __iter__(self):
    #     return iter(self.points)

    # Updates the IsoField distance values, based on the given sdf equation
    # @timeit
    def update(self, sdf_expr):
        # if not callable(sdf):
        #     raise RuntimeError("the given sdf equation function should be callable")
        # for p in self.points:
        #     p[-1] = sdf_expr(p[:-1])
        # x = self.points[:, 0]
        # y = self.points[:, 1]
        # z = self.points[:, 2]
        # local_dict = {'x':x, 'y':y, 'z':z}
        # self.points[:, 3] = ne.evaluate(sdf_expr, local_dict=local_dict)
        self.points[:, -1] = sdf_expr(self.points[:, :-1])

    def points_count(self) -> int:
        n = self.dim + np.array([1, 1, 1])
        return n[0]*n[1]*n[2]

    def cells_count(self) -> int:
        n = self.dim
        return n[0]*n[1]*n[2]

    # TODO: https://numpy.org/devdocs//reference/generated/numpy.vectorize.html
    def flat_point_id(self, id: np.array) -> int:
        # if id.shape[0] != 3:
        #     raise RuntimeError(f"the given id should be 3 integers, not {id.shape[0]}")
        n = self.dim + np.array([1, 1, 1])
        return id[0] * n[1] * n[2] + id[1] * n[2] + id[2]

    # TODO: https://numpy.org/devdocs//reference/generated/numpy.vectorize.html
    def flat_cell_id(self, id: np.array) -> int:
        # if id.shape[0] != 3:
        #     raise RuntimeError(f"the given id should be 3 integers, not {id.shape[0]}")
        n = self.dim
        return id[0] * n[1] * n[2] + id[1] * n[2] + id[2]

    def point_ids(self):
        for i in range(self.dim[0] + 1):
            for j in range(self.dim[1] + 1):
                for k in range(self.dim[2] + 1):
                    yield np.array([i, j, k])

    # generator for the ids of all non-boundary points
    def inner_point_ids(self):
        # for i in range(1, self.dim[0]):
        #     for j in range(1, self.dim[1]):
        #         for k in range(1, self.dim[2]):
        #             yield np.array([i, j, k])
        for i in range(0, self.dim[0]-1):
            for j in range(0, self.dim[1]-1):
                for k in range(0, self.dim[2]-1):
                    yield np.array([i, j, k])

    def cell_ids(self):
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                for k in range(self.dim[2]):
                    yield np.array([i, j, k])
