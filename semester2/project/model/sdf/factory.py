from model.mesh_factory import MeshFactory
# import numpy as np
import glm
from model.point_cloud import Vertex
from model.mesh import Mesh
# from model.sdf.equations import derivative
from model import sdf
# from model.util import sign
from sys import float_info
eps = float_info.epsilon

# TODO: Make such that the number of cubes is +1
# but with the same ratio and min_pos, so a sphere
# of radius one can be fully bounded by the field
# from (-1, -1, -1) to (1, 1, 1)

# def normal_xyz(n: glm.ivec3):
#     result = [glm.vec3(0, 0, 0)]*(n.x*n.y*n.z)
#     for i in range(n.x):
#         for j in range(n.y):
#             for k in range(n.z):
#                 id = i * n.y * n.z + j * n.z + k
#                 p = result[id]
#                 p.x = i/n.x,
#                 p.y = i/n.y,
#                 p.z = i/n.z,
#     return result


# Surface Nets
# https://bonsairobo.medium.com/smooth-voxel-mapping-a-technical-deep-dive-on-real-time-surface-nets-and-texturing-ef06d0f8ca14
# https://0fps.net/2012/07/10/smooth-voxel-terrain-part-1/
# https://0fps.net/2012/07/12/smooth-voxel-terrain-part-2/
# https://medium.com/@ryandremer/implementing-surface-nets-in-godot-f48ecd5f29ff
# https://www.researchgate.net/publication/371492555_SurfaceNets-Draft
# https://www.researchgate.net/publication/372871904_A_High-Performance_SurfaceNets_Discrete_Isocontouring_Algorithm
class Factory(MeshFactory):
    EDGES = (
        glm.ivec3(1, 0, 0),
        glm.ivec3(0, 1, 0),
        glm.ivec3(0, 0, 1),
    )
    QUADS = (
        (
            glm.ivec3(1, 0, 0),
            glm.ivec3(1, 1, 0),
            glm.ivec3(1, 1, 1),
            glm.ivec3(1, 0, 1),
        ),
        (
            glm.ivec3(0, 1, 1),
            glm.ivec3(1, 1, 1),
            glm.ivec3(1, 1, 0),
            glm.ivec3(0, 1, 0),
        ),
        (
            glm.ivec3(0, 0, 1),
            glm.ivec3(1, 0, 1),
            glm.ivec3(1, 1, 1),
            glm.ivec3(0, 1, 1),
        ),
    )
    CUBE_POINTS = (
        glm.ivec3(0, 0, 0),
        glm.ivec3(1, 0, 0),
        glm.ivec3(0, 1, 0),
        glm.ivec3(1, 1, 0),
        glm.ivec3(0, 0, 1),
        glm.ivec3(1, 0, 1),
        glm.ivec3(0, 1, 1),
        glm.ivec3(1, 1, 1),
    )

    CUBE_EDGES = (
        (glm.ivec3(0, 0, 0), glm.ivec3(1, 0, 0)),
        (glm.ivec3(1, 0, 0), glm.ivec3(1, 1, 0)),
        (glm.ivec3(1, 1, 0), glm.ivec3(0, 1, 0)),
        (glm.ivec3(0, 1, 0), glm.ivec3(0, 0, 0)),

        (glm.ivec3(0, 0, 1), glm.ivec3(1, 0, 1)),
        (glm.ivec3(1, 0, 1), glm.ivec3(1, 1, 1)),
        (glm.ivec3(1, 1, 1), glm.ivec3(0, 1, 1)),
        (glm.ivec3(0, 1, 1), glm.ivec3(0, 0, 1)),

        (glm.ivec3(0, 0, 0), glm.ivec3(0, 0, 1)),
        (glm.ivec3(1, 0, 0), glm.ivec3(1, 0, 1)),
        (glm.ivec3(1, 1, 0), glm.ivec3(1, 1, 1)),
        (glm.ivec3(0, 1, 0), glm.ivec3(0, 1, 1)),
    )

    # a 3d point field from (-1, -1, -1) to (1, 1, 1)
    def points(self):
        for i in range(self.n.x + 1):
            for j in range(self.n.y + 1):
                for k in range(self.n.z + 1):
                    scale = self.max_pos - self.min_pos
                    offset = self.min_pos
                    yield glm.vec3(
                        i/self.n.x,
                        j/self.n.y,
                        k/self.n.z,
                    ) * scale + offset

    def __init__(self, dim: glm.ivec3, min_pos=glm.vec3(-1, -1, -1), max_pos=glm.vec3(1, 1, 1)):
        self.n = glm.ivec3(dim)
        self.min_pos = glm.vec3(min_pos)
        self.max_pos = glm.vec3(max_pos)
        # we will use the 4th coordinate to cache the sdf value
        self.grid = [glm.vec4(p.x, p.y, p.z, 0.0) for p in self.points()]

    def flat_point_id(self, id: glm.ivec3) -> int:
        n = self.n + glm.ivec3(1, 1, 1)
        return id.x * n.y * n.z + id.y * n.z + id.z

    # def grid_id(self, id: int) -> glm.ivec3:
    #     return glm.ivec3(
    #         id,
    #         id,
    #         id % self.n.z,
    #     )

    def calc_sdf(self, sdf):
        if not callable(sdf):
            raise RuntimeError("the given sdf equation function should be callable")
        for p in self.grid:
            p.w = sdf(glm.vec3(p.x, p.y, p.z))

    # def cube_center(self, cube_id: glm.ivec3) -> glm.vec3:
    #     p = glm.vec3(0.0, 0.0, 0.0)
    #     for diff in Factory.CUBE_POINTS:
    #         i = cube_id + diff
    #         p += glm.vec3(self.grid[self.flat_point_id(i)])
    #     return p / len(Factory.CUBE_POINTS)

    def cube_center(self, cube_id: glm.ivec3) -> glm.vec3:
        edge_mids = list()
        for edge in Factory.CUBE_EDGES:
            ep = [cube_id + i for i in edge]
            back = self.grid[self.flat_point_id(ep[0])]
            front = self.grid[self.flat_point_id(ep[1])]
            if front.w * back.w < 0.0:
                h = abs(front.w) / (abs(front.w - back.w))
                edge_mids.append(glm.lerp(glm.vec3(front), glm.vec3(back), h))
        if len(edge_mids) == 0:
            raise RuntimeError("You need at least one of the cube edges to intersect with the surface")
        return sum(edge_mids) / len(edge_mids)

    def point_ids(self):
        for i in range(self.n.x + 1):
            for j in range(self.n.y + 1):
                for k in range(self.n.z + 1):
                    yield glm.ivec3(i, j, k)

    def inner_point_ids(self):
        for i in range(1, self.n.x):
            for j in range(1, self.n.y):
                for k in range(1, self.n.z):
                    yield glm.ivec3(i, j, k)

    def cube_ids(self):
        for i in range(self.n.x):
            for j in range(self.n.y):
                for k in range(self.n.z):
                    yield glm.ivec3(i, j, k)

    def get_mesh(self, eq):
        self.calc_sdf(eq)
        field_to_mesh = dict()  # point field id to its flat id in the mesh
        mesh = Mesh()

        for point_id in self.inner_point_ids():
            for e, q in zip(Factory.EDGES, Factory.QUADS):
                ONE = glm.ivec3(1, 1, 1)
                back = self.grid[self.flat_point_id(point_id)].w
                front = self.grid[self.flat_point_id(point_id + e)].w
                # if sign(back) != sign(front):
                if back * front < 0.0:
                    quad_ids = [point_id + x for x in q]
                    if front < 0.0:
                        quad_ids = reversed(quad_ids)
                    mesh.faces.append(list())
                    # TODO: if back is -1 use quad, else use reversed quad
                    for qp in quad_ids:
                        if qp in field_to_mesh:
                            mesh.faces[-1].append(field_to_mesh[qp])
                        else:
                            field_to_mesh[qp] = len(mesh.points)
                            mesh.faces[-1].append(len(mesh.points))
                            mesh.points.append(Vertex(self.cube_center(qp - ONE)))

        # gradient descend
        for p in mesh.points:
            p.norm = glm.normalize(sdf.gradient(p.pos, eq))
            p.pos -= eq(p.pos) * p.norm

        return mesh
