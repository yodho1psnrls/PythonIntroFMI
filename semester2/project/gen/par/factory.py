from gen.mesh_factory import MeshFactory
import numpy as np
# import glm
from gen.mesh import Mesh
# from gen.vertex import Vertex
# import parametric as par
from gen import par

# TODO: Make the grid with 3d uvs that if different than 0
# will be used with the gradient as bump map


# Factory class that converts and
# Equation to a 3D mesh
class Factory(MeshFactory):
    def __init__(self, rows: int, cols: int):
        self.grid = par.QuadGrid(rows, cols)
        # points = [
        #     Vertex(glm.vec3(uv.x, uv.y, 0), glm.vec3(0, 0, 1), uv)
        #     for uv in self.grid.points()
        # ],
        # self.mesh = Mesh(points, self.grid.faces())

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
        mesh = Mesh(self.grid.points, self.grid.faces)
        # mesh = Mesh(self.grid.points.copy(), self.grid.faces.copy())
        for p in mesh.points:
            # h = 0.5 * (1 / self.grid.dim.x + 1/self.grid.dim.y)
            h = par.eps
            p['norm'] = par.gradient(p['uv'], eq, h)
            p['norm'] /= np.linalg.norm(p['norm'])
            p['pos'] = eq(p['uv'])
        # points = [eq(uv) for uv in self.grid.points()]
        # faces = self.grid.faces()
        # return Mesh(points, faces)
        return mesh
