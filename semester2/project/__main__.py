# import gen.parametric as par
from gen.mesh import Mesh
from gen.mesh import polygon_diagonals
from gen.point_cloud import PointCloud
from gen.point_cloud import vertex_dtype
# from gen.vertex import Vertex
from gen import par
from gen import sdf
from view.plot import ViewSystem
import numpy as np
# import glm
from render.render_system import RenderSystem
from gen.par.grid import QuadGrid
import time
import gen.util as u
from math import pi


if __name__ == '__main__':
    gen = sdf.Factory(
        (36, 36, 36),
        # (126, 126, 126),
        (-1.25, -1.25, -1.25),
        (1.25, 1.25, 1.25),
    )

    # rot = u.orientate((1, 1, 1), (0, 0, 1))
    # rot @= u.orientate((0, 0, 1), (0, 1, 0))
    # eq = lambda p: sdf.polynomial_degree3(0.675*p@np.linalg.inv(rot))
    # eq = sdf.Torus(0.75, 0.25)
    # eq = sdf.Sphere(0.75)

    # sphere = sdf.Equation("sqrt(x**2+y**2+z**2)-0.75")
    # return (1-3*x-3*y-3*z)*(x*y+x*z+y*z)+6*x*y*z
    eq = sdf.Equation("(1-3*x-3*y-3*z)*(x*y+x*z+y*z)+6*x*y*z")
    plane = sdf.Equation("y")

    mesh = gen.get_mesh(eq)
    # mesh.invert()
    # mesh.triangulate()
    # mesh.update_normals()

    print(f"points: {len(mesh.points)}")
    print(f"faces: {len(mesh.faces)}")

    pl = ViewSystem()
    pl.draw_mesh(mesh)
    # pl.draw_normals(mesh)
    # mesh.save("blqblq")

    # eng = Engine()
    # eng.load_mesh(mesh)
    # eng.run()
