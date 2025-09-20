import numpy as np


class PointCloud:
    # points: list of 3d vectors
    def __init__(
        self,
        points: list[np.array],
    ):
        self.points = list(map(np.array, points))
