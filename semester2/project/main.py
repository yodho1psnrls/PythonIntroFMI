# import model.parametric as par
from model.mesh import Mesh
from model import par
import view.plot as pl
import numpy as np


class Foo:
    def __init__(self, x):
        self.x = x

    def calc(self, y):
        return self.x + y

    def __call__(self, y):
        return self.x + y


def for_each(func, vals: list):
    return [func(x) for x in vals]


if __name__ == '__main__':
    # points = [np.array([uv[0], uv[1], 0]) for uv in par.normal_uvs(4, 4)]
    # points = [[uv[0], uv[1], 0] for uv in par.normal_uvs(4, 4)]
    # grid = par.quad_ids(4, 4)
    # mesh = Mesh(points, grid)
    # for p in mesh.points:
    #     print(p)
    # for quad in mesh.faces:
    #     print(quad)

    gen = par.Factory(16, 16)
    # eq = par.Cone()
    eq = par.cone
    mesh = gen.get_mesh(eq)

    print(type(mesh.points[0]))
    print(f"points: {len(mesh.points)}")
    print(f"quads: {len(mesh.faces)}")
    # print(issubclass(par.Generator, par.MeshFactory))
    pl.draw(mesh)
