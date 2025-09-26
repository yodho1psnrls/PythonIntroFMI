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


if __name__ == '__main__':
    gen = sdf.Factory(
        (126, 126, 126),
        (-1.25, -1.25, -1.25),
        (1.25, 1.25, 1.25),
    )

    rot = u.orientate((1, 1, 1), (0, 0, 1))
    rot @= u.orientate((0, 0, 1), (0, 1, 0))
    eq = lambda p: sdf.polynomial_degree3(0.675*p@np.linalg.inv(rot))
    # eq = sdf.Torus(0.75, 0.25)
    # eq = sdf.Sphere(0.75)

    mesh = gen.get_mesh(eq)
    mesh.invert()
    # mesh.triangulate()
    # mesh.update_normals()

    print(f"points: {len(mesh.points)}")
    print(f"faces: {len(mesh.faces)}")

    pl = ViewSystem()
    # pl.draw_mesh(mesh)
    # pl.draw_normals(mesh)
    mesh.save("blqblq")

    # eng = Engine()
    # eng.load_mesh(mesh)
    # eng.run()
