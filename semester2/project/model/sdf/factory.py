from model.mesh_factory import MeshFactory
# import numpy as np
import glm
from model.mesh import Mesh
# import parametric as par
from model import par
from model.util import sign


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

def normal_xyz(n: glm.ivec3):
    for i in range(n.x):
        for j in range(n.y):
            for k in range(n.z):
                yield glm.vec3(
                    i/n.x,
                    j/n.y,
                    k/n.z,
                )


# Surface Nets
# https://medium.com/@ryandremer/implementing-surface-nets-in-godot-f48ecd5f29ff
# https://www.researchgate.net/publication/371492555_SurfaceNets-Draft
# https://www.researchgate.net/publication/372871904_A_High-Performance_SurfaceNets_Discrete_Isocontouring_Algorithm
class Factory(MeshFactory):
    EDGES = [
        glm.ivec3(1, 0, 0),
        glm.ivec3(0, 1, 0),
        glm.ivec3(0, 0, 1),
    ]
    QUADS = [
        [
            glm.ivec3(0, 0, 0),
            glm.ivec3(0, 1, 0),
            glm.ivec3(0, 1, 1),
            glm.ivec3(0, 0, 1),
        ],
        [
            glm.ivec3(0, 0, 0),
            glm.ivec3(1, 0, 0),
            glm.ivec3(1, 0, 1),
            glm.ivec3(0, 0, 1),
        ],
        [
            glm.ivec3(0, 0, 0),
            glm.ivec3(1, 0, 0),
            glm.ivec3(1, 1, 0),
            glm.ivec3(0, 1, 0),
        ],
    ]
    CUBE = [
        glm.ivec3(0, 0, 0),
        glm.ivec3(1, 0, 0),
        glm.ivec3(0, 1, 0),
        glm.ivec3(1, 1, 0),
        glm.ivec3(0, 0, 1),
        glm.ivec3(1, 0, 1),
        glm.ivec3(0, 1, 1),
        glm.ivec3(1, 1, 1),
    ]
    def __init__(self, numX: int, numY: int, numZ: int):
        self.n = glm.ivec3(numX, numY, numZ)
        # we will use the 4th coordinate to cache the sdf value
        self.grid = [glm.vec4(p.x, p.y, p.z, 0.0) for p in normal_xyz(self.n)]

    def flat_id(self, id: glm.ivec3) -> int:
        n = self.n
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
            p.w = sdf(glm.vec(p.x, p.y, p.z))

    def calc_point(self, id: glm.ivec3) -> glm.vec3:
        p = glm.vec3(0.0, 0.0, 0.0)
        for diff in CUBE:
            i = id + diff
            p += glm.vec3(self.grid[self.flat_id(i)])
        return p / 8.0

    def get_mesh(self, sdf):
        self.calc_sdf(sdf)
        points = dict()
        quads = list()
        for i in range(n.x):
            for j in range(n.y):
                for k in range(n.z):
                    id = glm.ivec3(i, j, k)
                    for e in Factory.EDGES:
                        back = self.points[self.flat_id(id)].w
                        front = self.points[self.flat_id(id+e)].w
                        if sign(back) != sign(front):

        



