# import glm
import numpy as np
from model.mesh import Mesh
# from model.vertex import Vertex
# from math import floor


# uv coordinates from 0 to 1
def normal_uvs(rows: int, cols: int):
    # result = list()
    for i in range(rows+1):
        for j in range(cols+1):
            # result.append(glm.vec2(
            yield (
                float(i / rows),
                float(j / cols),
            )
    # return result


# generates a quad grid of rows by columns
def quad_ids(rows: int, cols: int):
    # result = list()
    for i in range(rows):
        for j in range(cols):
            # result.append([
            yield (
                (i+1)*(cols+1) + j,
                (i+1)*(cols+1) + (j+1),
                i*(cols+1) + (j+1),
                i*(cols+1) + j,
            )
    # return result


class QuadGrid(Mesh):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # points = [
        #     Vertex(glm.vec3(uv.x, uv.y, 0), glm.vec3(0, 0, 1), uv) for uv in normal_uvs(dim.x, dim.y)
        # ],
        super().__init__(
            [((uv[0], uv[1], 0), (0, 0, 1), uv) for uv in normal_uvs(rows, cols)],
            list(quad_ids(rows, cols))
        )

    # def point_count(self) -> int:
    #     return (self.dim.x + 1) * (self.dim.y + 1)
    #
    # def face_count(self) -> int:
    #     return self.dim.x * self.dim.y

    # def points(self):   # returns 2D uv coordinates !!!
    #     return normal_uvs(self.dim.x, self.dim.y)
    #
    # def faces(self):
    #     return quad_ids(self.dim.x, self.dim.y)

    '''
    def grid_point_id(self, id: int) -> glm.ivec2:
        py = self.dim.y+1
        return glm.ivec2(floor(id / py), id % py)

    def grid_face_id(self, id: int) -> glm.ivec2:
        py = self.dim.y
        return glm.ivec2(floor(id / py), id % py)

    def flat_point_id(self, id: glm.ivec2) -> int:
        return id.x * (self.dim.y+1) + id.y

    def flat_face_id(self, id: glm.ivec2) -> int:
        return id.x * self.dim.y + id.y

    def is_valid_point_id(self, id: glm.ivec2) -> bool:
        return (0 <= id.x and id.x < (self.dim.x + 1)) and (0 <= id.y and id.y < (self.dim.y + 1))

    def is_valid_face_id(self, id: glm.ivec2) -> bool:
        return (0 <= id.x and id.x < self.dim.x) and (0 <= id.y and id.y < self.dim.y)

    # given a point_id, it returns the
    #  ids of the neighbouring points
    def point_to_points(self, id: int):
        if not self.is_valid_point_id(id):
            raise RuntimeError("Invalid point id")
        result = list()
        grid_id = self.grid_point_id(id)
        IDs = [
            glm.ivec2(-1, -1),
            glm.ivec2(1, -1),
            glm.ivec2(1, 1),
            glm.ivec2(-1, 1),
        ]
        for i in IDs:
            other_id = grid_id + i
            if self.is_valid_point_id(other_id):
                result.append(self.flat_point_id(other_id))
        return result

    # given a point_id, it returns the
    #  ids of the neighbouring points
    def face_to_points(self, id: int):
        if not self.is_valid_face_id(id):
            raise RuntimeError("Invalid face id")
        grid_id = self.grid_face_id(id)
        IDs = [
            glm.ivec2(0, 0),
            glm.ivec2(1, 0),
            glm.ivec2(1, 1),
            glm.ivec2(0, 1),
        ]
        return [self.flat_point_id(grid_id + i) for i in IDs]
    '''


# class RegularGrid:
#     def __init__(self, sides: int, dim: glm.ivec2):
#         pass
