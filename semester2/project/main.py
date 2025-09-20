# import model.parametric as par
from model.mesh import Mesh
from model import par
import view.plot as pl
import numpy as np

if __name__ == '__main__':
    # points = [np.array([uv[0], uv[1], 0]) for uv in par.normal_uvs(4, 4)]
    # points = [[uv[0], uv[1], 0] for uv in par.normal_uvs(4, 4)]
    # grid = par.quad_ids(4, 4)
    # mesh = Mesh(points, grid)
    # for p in mesh.points:
    #     print(p)
    # for quad in mesh.indices:
    #     print(quad)
    # print(type(mesh.points[0]))

    gen = par.Generator(16, 16)
    # eq = par.Shere(1.0)
    eq = par.Cone()
    mesh = gen.get_mesh(eq)

    print(f"points: {len(mesh.points)}")
    print(f"quads: {len(mesh.indices)}")
    pl.draw(mesh)
