import numpy as np
from model.sdf.iso_field import IsoField
from model.util import AXIS
from model.mesh_factory import MeshFactory
from model.mesh import Mesh
from model.point_cloud import vertex_dtype
from model.sdf import gradient
from model.util import lerp
from model.util import timeit
import time
ONE = np.ones((3), dtype=np.int32)

# TODO: Make such that the number of cubes is +1
# but with the same ratio and min_pos, so a sphere
# of radius one can be fully bounded by the field
# from (-1, -1, -1) to (1, 1, 1)

# NOTE: You can also cache a bitmask for all edges
# that gives 1 or 0 if the edge is intersecting with the surface
# and then in the bilinear interpolation for the cube center
# you can add them branchlessly and then always divide by 8


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
        (  # quad facing toward x
            (1, 0, 0),
            (1, 1, 0),
            (1, 1, 1),
            (1, 0, 1),
        ),
        (  # quad facing toward y
            (0, 1, 1),
            (1, 1, 1),
            (1, 1, 0),
            (0, 1, 0),
        ),
        (  # quad facing toward z
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
        # Used when generating mesh with sparse point indexing in the faces
        # self.cell_centers = np.zeros((self.cells_count()), dtype=vertex_dtype)
        # for c in self.cell_ids():
        #     self.cell_centers[self.flat_cell_id(c)][0] = self.cell_center(c)

        # 12.5% speedup by caching all possible edge ids for fast iteration
        nx, ny, nz = self.dim - np.ones((3), dtype=np.int32)
        self.all_edge_ids = np.array(list(np.ndindex((nx, ny, nz, 3))), dtype=np.int32)
        # self.iter_point_ids = np.ndindex((nx, ny, nz))
        # self.iter_point_ids = np.vstack(np.meshgrid(
        #     np.arange(nx),
        #     np.arange(ny),
        #     np.arange(nz),
        #     indexing='ij'
        # ))

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
            if front[-1] * back[-1] <= 0.0:
                h = abs(front[-1]) / (abs(front[-1] - back[-1]))
                center += lerp(front[:-1], back[:-1], h)
                num_edges += 1
        if num_edges == 0:
            raise RuntimeError("You need at least one of the cube edges to intersect with the surface")
        return center / num_edges

    def valid_edges(self):
        edge_axes = self.all_edge_ids[:, -1]
        point_ids = self.all_edge_ids[:, :-1]

        # The back and front edge global point ids
        back_ids = point_ids + ONE
        front_ids = point_ids + ONE + AXIS[edge_axes]

        n = self.dim + ONE
        back_flat = back_ids[:, 0]*n[1]*n[2] + back_ids[:, 1]*n[2] + back_ids[:, 2]
        front_flat = front_ids[:, 0]*n[1]*n[2] + front_ids[:, 1]*n[2] + front_ids[:, 2]
        # back_flat = [self.flat_point_id(i) for i in back_ids]
        # front_flat = [self.flat_point_id(i) for i in front_ids]

        back = self.points[back_flat, -1]
        front = self.points[front_flat, -1]
        mask = back * front <= 0.0
        return np.nonzero(mask)[0]

    '''
    def generate_quads(self):
        quads = []
        for edge_id in self.all_edge_ids:
            e = AXIS[edge_id[-1]]
            q = Factory.QUADS_PER_AXIS[edge_id[-1]]  # local quad point ids
            point_id = edge_id[:-1]
            back = self.points[self.flat_point_id(ONE+point_id)][-1]
            front = self.points[self.flat_point_id(ONE+point_id + e)][-1]
            if back * front <= 0.0:
                quad_ids = q + point_id  # global quad point ids
                if front <= 0.0:  # reverse for consistent orientation
                    quad_ids = quad_ids[::-1]
                quads.append([self.flat_cell_id(cell_id) for cell_id in quad_ids])
        return quads
    '''

    # NOTE: This gives the generated quads
    # But each of the quads store the 3d field point ids
    # not the flattened ids !
    def generate_quads(self):
        point_ids = self.all_edge_ids[:, :-1]  # shape(n, 3)
        edge_axis = self.all_edge_ids[:, -1]   # shape(n)

        # All edges (3d coords of their back and front points on the grid/field)
        back_ids = point_ids + ONE
        front_ids = point_ids + ONE + AXIS[edge_axis]

        # All edges (flattened 1D coords of their back and front points on the grid/field)
        pd = self.dim + ONE  # points dim
        back_flat = back_ids[:, 0]*pd[1]*pd[2] + back_ids[:, 1]*pd[2] + back_ids[:, 2]
        front_flat = front_ids[:, 0]*pd[1]*pd[2] + front_ids[:, 1]*pd[2] + front_ids[:, 2]

        # The back and front sd values of all edges
        back = self.points[back_flat, -1]
        front = self.points[front_flat, -1]

        valid_edge_ids = np.nonzero(back * front <= 0.0)[0]
        valid_points = point_ids[valid_edge_ids]
        valid_axis = edge_axis[valid_edge_ids]

        # Local quad 3d point ids per axis (with shape (num_valid_axis, 4, 3))
        local_quads = Factory.QUADS_PER_AXIS[valid_axis]
        # print("local_quads", local_quads.shape)
        # Offset by the valid point 3d indexes,
        # to get the global 3d indexes of each point in the quad
        # (we use np.newaxis, since we dont want to add the point offsets
        #  to the quads, but to the 3d local point ids that they store)
        quads = local_quads + valid_points[:, np.newaxis, :]
        # print("global_quads", quads.shape)

        # Reverse quads in opposite direction for consistent orientation
        valid_front = front[valid_edge_ids]
        rev_mask = valid_front <= 0.0
        quads[rev_mask] = quads[rev_mask, ::-1, :]

        # Convert quads from storing 3d point ids
        # to store flat point ids
        # flat_quads = (
        #     quads[:, :, 0]*self.dim[1]*self.dim[2] +
        #     quads[:, :, 1]*self.dim[2] +
        #     quads[:, :, 2]
        # )
        # return flat_quads
        return quads

    # @timeit
    def get_mesh(self, eq):
        start = time.time()
        super().update(eq)
        end = time.time()
        print(f"Field: {end-start}")

        start = time.time()
        quads = self.generate_quads()
        # Get the valid 3d cell ids, and remap the quads to point to them
        indices = quads.reshape((len(quads)*4, 3))
        cells_in_use, quads = np.unique(indices, return_inverse=True, axis=0)
        quads = quads.reshape((len(quads)//4, 4))
        mesh = Mesh(
            [(self.cell_center(i), (0.0, 0.0, 0.0), (0.0, 0.0)) for i in cells_in_use],
            quads
        )
        end = time.time()
        print(f"Mesh: {end-start}")

        # mesh = Mesh(np.copy(self.cell_centers), quads)
        # mesh.trim()

        # gradient descend
        start = time.time()
        for p in mesh.points:
            p['norm'] = gradient(p['pos'], eq)
            p['norm'] /= np.linalg.norm(p['norm'])
            p['pos'] -= eq(p['pos']) * p['norm']
        end = time.time()
        print(f"Gradient: {end-start}")

        return mesh
