from model.vertex import Vertex


class PointCloud:
    # points: list of 3d vectors
    def __init__(
        self,
        points: list[Vertex] = None,
    ):
        # self.points = list(map(Vertex, points))
        # self.points = list(points)
        self.points = list(points) if points else []

    # def __sum__()
