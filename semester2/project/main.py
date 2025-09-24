# import model.parametric as par
from model.mesh import Mesh
from model.mesh import polygon_diagonals
from model.point_cloud import PointCloud
from model.point_cloud import vertex_dtype
# from model.vertex import Vertex
from model import par
from model import sdf
from view.plot import ViewSystem
import numpy as np
# import glm
from view.engine import Engine
from model.par.grid import QuadGrid
import time
import model.util as u
from math import pi


class Foo:
    def __init__(self, x):
        self.x = x

    def calc(self, y):
        return self.x + y

    def __call__(self, y):
        return self.x + y


def for_each(func, vals: list):
    return [func(x) for x in vals]


# if __name__ == '__main__':
    # eng = Engine()
    # eng.run()
    # mesh = QuadGrid(2, 2)
    # print(mesh.positions)
    # arr = np.array([1, 2, 3, 4])
    # arr2 = np.array(arr)
    # print(arr2)
    # mesh = Mesh(
    #     np.zeros((10), dtype=vertex_dtype),
    #     [
    #         [2, 4, 6],
    #         [3, 4, 6],
    #     ]
    # )
    # mesh.trim()
    # for p in mesh.faces:
    #     print(p)


if __name__ == '__main__':
    pl = ViewSystem()

    # BUG:
    # pts = [uv for uv in gen.grid.points()],
    # pts = list(gen.grid.points())
    # pts = [uv for uv in par.normal_uvs(16, 16)],
    # pts = list(par.normal_uvs(16, 16))
    # print(f"points: {len(pts)}")

    # gen = par.Factory(24, 24)
    # mesh = gen.get_mesh(par.cone)
    # mesh = gen.get_mesh(par.sphere)
    # mesh = gen.grid

    gen = sdf.Factory(
        # (16, 16, 16),
        # (32, 32, 32),
        (66, 66, 66),
        # (126, 126, 126),
        (-1.25, -1.25, -1.25),
        (1.25, 1.25, 1.25),
    )
    # mesh = gen.get_mesh(sdf.pumpkin)
    # mesh = gen.get_mesh(sdf.Sphere())
    start = time.time()
    mesh = gen.get_mesh(sdf.Torus(0.75, 0.25))
    # eq = lambda p: np.linalg.norm(p-np.array([1.0, 1.0, 1.0])) - 1.0
    # rot = u.orientate((1, 1, 1), (0, 0, 1))
    # rot @= u.orientate((0, 0, 1), (0, 1, 0))
    # eq = lambda p: sdf.polynomial_degree3(0.675*p@np.linalg.inv(rot))
    # rot = u.orientate((0, 0, 1), (1, 1, 1))
    # cap = sdf.Capsule((0, 0, 0.0), (0, 0, 0.85), 0.15)
    # eq = lambda p: cap(p@np.linalg.inv(rot))
    # mesh = gen.get_mesh(eq)
    # mesh = gen.get_mesh(sdf.Sphere())
    # mesh = gen.get_mesh(sdf.polynomial_degree3)
    end = time.time()
    print(f"{end-start}s")
    # print(f"{(end-start)*1000}ms")

    # mesh.trim()
    # mesh.triangulate()
    # mesh.update_normals()
    # for p in mesh.points:
    #     p['pos'] += p['norm'] * 0.25

    # mat = np.linalg.inv(u.look_at(np.array([1, 0, 0])))
    # mat @= u.look_at(np.array([0, 1, 0]))
    # mat = u.look_at(np.array([1.0, 0.0, 0.0]))
    # mat = u.rotate([1, -1, 0], pi/6)
    # mat = u.orientate((1, 1, 1), (0, 0, 1))
    # for p in mesh.positions:
    #     p @= rot
        # p = (np.append(p, 1.0) @ mat)[:-1]

    print(f"points: {len(mesh.points)}")
    print(f"faces: {len(mesh.faces)}")
    # print(issubclass(par.Generator, par.MeshFactory))

    # mesh.save("blqblq")
    # pl.draw_normals(mesh)
    pl.draw_mesh(mesh)
    # pl.draw_points(PointCloud(mesh.points))

    # gen = sdf.Factory(glm.ivec3(2, 2, 2))
    # pc = PointCloud(gen.points())
    # print(len(pc.points))
    # pl.draw_points(pc)
