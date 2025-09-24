import numpy as np
from model.sdf.iso_field import IsoField
from model.util import AXIS
from model.mesh_factory import MeshFactory
from model.mesh import Mesh
from model.point_cloud import vertex_dtype
from model.sdf import gradient
from model.util import lerp

# TODO: Make such that the number of cubes is +1
# but with the same ratio and min_pos, so a sphere
# of radius one can be fully bounded by the field
# from (-1, -1, -1) to (1, 1, 1)


# Surface Nets
# https://bonsairobo.medium.com/smooth-voxel-mapping-a-technical-deep-dive-on-real-time-surface-nets-and-texturing-ef06d0f8ca14
# https://0fps.net/2012/07/10/smooth-voxel-terrain-part-1/
# https://0fps.net/2012/07/12/smooth-voxel-terrain-part-2/
# https://medium.com/@ryandremer/implementing-surface-nets-in-godot-f48ecd5f29ff
# https://www.researchgate.net/publication/371492555_SurfaceNets-Draft
# https://www.researchgate.net/publication/372871904_A_High-Performance_SurfaceNets_Discrete_Isocontouring_Algorithm
# class Factory(MeshFactory, IsoField):
class Factory(IsoField):
    QUADS_PER_AXIS = np.array([
        (
            (1, 0, 0),
            (1, 1, 0),
            (1, 1, 1),
            (1, 0, 1),
        ),
        (
            (0, 1, 1),
            (1, 1, 1),
            (1, 1, 0),
            (0, 1, 0),
        ),
        (
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (0, 1, 1),
        ),
    ])
    CUBE_POINTS = np.array([
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, 0),
        (0, 0, 1),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
    ])

    CUBE_EDGES = np.array([
        ((0, 0, 0), (1, 0, 0)),
        ((1, 0, 0), (1, 1, 0)),
        ((1, 1, 0), (0, 1, 0)),
        ((0, 1, 0), (0, 0, 0)),

        ((0, 0, 1), (1, 0, 1)),
        ((1, 0, 1), (1, 1, 1)),
        ((1, 1, 1), (0, 1, 1)),
        ((0, 1, 1), (0, 0, 1)),

        ((0, 0, 0), (0, 0, 1)),
        ((1, 0, 0), (1, 0, 1)),
        ((1, 1, 0), (1, 1, 1)),
        ((0, 1, 0), (0, 1, 1)),
    ])

    def possible_quads(self) -> int:
        n = self.dim - np.array([1, 1, 1])
        return 3*n[0]*n[1]*n[2]

    def __init__(self, dim: list[int], min_pos=[-1, -1, -1], max_pos=[1, 1, 1]):
        super().__init__(dim, min_pos, max_pos)
        # Cache the cell centers
        # self.cell_centers = np.zeros((self.cells_count()), dtype=vertex_dtype)
        # for c in self.cell_ids():
        #     self.cell_centers[self.flat_cell_id(c)][0] = self.cell_center(c)

    # def cell_center(self, cell_id: np.array) -> np.array:
    #     p = np.zeros((3), dtype=np.float32)
    #     for diff in Factory.CUBE_POINTS:
    #         i = cell_id + diff
    #         p += self.points[self.flat_point_id(i)][:-1]
    #     return p / len(Factory.CUBE_POINTS)

    def cell_center(self, cell_id: np.array) -> np.array:
        if cell_id.shape[0] != 3:
            raise RuntimeError("the given id should be 3 integers")
        center = np.zeros((3), dtype=np.float32)
        num_edges = 0
        for edge in Factory.CUBE_EDGES:
            ep = [cell_id + i for i in edge]
            back = self.points[self.flat_point_id(ep[0])]
            front = self.points[self.flat_point_id(ep[1])]
            if front[-1] * back[-1] < 0.0:
                h = abs(front[-1]) / (abs(front[-1] - back[-1]))
                center += lerp(front[:-1], back[:-1], h)
                num_edges += 1
        if num_edges == 0:
            raise RuntimeError("You need at least one of the cube edges to intersect with the surface")
        return center / num_edges

    # NOTE: You can also cache a bitmask for all edges
    # that gives 1 or 0 if the edge is intersecting with the surface
    # and then in the bilinear interpolation for the cube center
    # you can add them branchlessly and then always divide by 8
    def get_mesh(self, eq):
        super().update(eq)
        faces = []
        points = []
        field_to_mesh_point_id = np.full(self.cells_count(), -1, dtype=np.int32)
        for point_id in self.inner_point_ids():
            for e, q in zip(AXIS, Factory.QUADS_PER_AXIS):
                ONE = np.ones((3), dtype=np.int32)
                back = self.points[self.flat_point_id(ONE+point_id)][-1]
                front = self.points[self.flat_point_id(ONE+point_id + e)][-1]
                # if sign(back) != sign(front):
                if back * front < 0.0:
                    quad_ids = q + point_id
                    if front < 0.0:  # reverse for consistent orientation
                        quad_ids = quad_ids[::-1]
                    faces.append([])
                    for cell_id in quad_ids:
                        flat_id = self.flat_cell_id(cell_id)
                        if field_to_mesh_point_id[flat_id] == -1:
                            field_to_mesh_point_id[flat_id] = len(points)
                            points.append(self.cell_center(cell_id))
                        faces[-1].append(field_to_mesh_point_id[flat_id])

        mesh = Mesh(
            [(p, (0.0, 0.0, 0.0), (0.0, 0.0)) for p in points],
            faces
        )

        # gradient descend
        for p in mesh.points:
            p['norm'] = gradient(p['pos'], eq)
            p['norm'] /= np.linalg.norm(p['norm'])
            p['pos'] -= eq(p['pos']) * p['norm']

        return mesh
