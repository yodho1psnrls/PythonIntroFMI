from model.mesh_factory import MeshFactory
# import numpy as np
import glm
from model.mesh import Mesh
# import parametric as par
from model import par


# uv coordinates from 0 to 1
def normal_uvs(rows: int, cols: int):
    for i in range(rows+1):
        for j in range(cols+1):
            yield glm.vec2(
                float(i / rows),
                float(j / cols),
            )


# generates a quad grid of rows by columns
def quad_ids(rows: int, cols: int):
    for i in range(rows):
        for j in range(cols):
            yield [
                i*(cols+1) + j,
                i*(cols+1) + (j+1),
                (i+1)*(cols+1) + (j+1),
                (i+1)*(cols+1) + j,
            ]


# Factory class that converts and
# Equation to a 3D mesh
class Factory(MeshFactory):
    def __init__(self, rows: int, cols=None):
        self.rows = rows
        self.cols = cols

    # def set_dim(self, rows, cols):
    #     self.rows = rows
    #     self.cols = cols

    # def get_mesh(self, eq: par.Equation) -> Mesh:
    #     points = [eq.calc(uv) for uv in normal_uvs(self.rows, self.cols)]
    #     quads = quad_ids(self.rows, self.cols)
    #     return Mesh(points, quads)

    def get_mesh(self, eq) -> Mesh:
        if not callable(eq):
            raise RuntimeError("the given equation function should be callable")
        points = [eq(uv) for uv in normal_uvs(self.rows, self.cols)]
        quads = quad_ids(self.rows, self.cols)
        return Mesh(points, quads)
