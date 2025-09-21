# import model.parametric as par
from model.mesh import Mesh
from model.point_cloud import PointCloud
from model.point_cloud import Vertex
from model import par
from model import sdf
from view.plot import ViewSystem
# import numpy as np
import glm


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
    pl = ViewSystem()

    # gen = par.Factory(16, 16)
    # mesh = gen.get_mesh(par.cone)
    # # mesh = gen.get_mesh(par.sphere)
    # # mesh = Mesh(gen.grid.points, gen.grid.faces)

    # BUG:
    # pts = [uv for uv in gen.grid.points()],
    # pts = list(gen.grid.points())
    # pts = [uv for uv in par.normal_uvs(16, 16)],
    # pts = list(par.normal_uvs(16, 16))
    # print(f"points: {len(pts)}")

    gen = sdf.Factory(
        glm.ivec3(22, 22, 22),
        glm.vec3(-1.15, -1.15, -1.15),
        glm.vec3(1.15, 1.15, 1.15),
    )

    # mesh = gen.get_mesh(sdf.Sphere())
    mesh = gen.get_mesh(sdf.Torus(0.75, 0.25))

    for p in mesh.points:
        p.pos += p.norm * 0.25

    print(type(mesh.points[0].pos))
    print(f"points: {len(mesh.points)}")
    print(f"quads: {len(mesh.faces)}")
    # print(issubclass(par.Generator, par.MeshFactory))
    mesh.save("blqblq.obj")
    pl.draw_mesh(mesh)
    # pl.draw_points(PointCloud(mesh.points))

    # gen = sdf.Factory(glm.ivec3(2, 2, 2))
    # pc = PointCloud(gen.points())
    # print(len(pc.points))
    # pl.draw_points(pc)

