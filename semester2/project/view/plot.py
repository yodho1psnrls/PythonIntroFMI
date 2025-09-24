import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from model.mesh import Mesh
from model.point_cloud import PointCloud


class ViewSystem:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        # self.ax.auto_scale_xyz(1.0, 1.0, 1.0)
        # self.ax.auto_scale_xyz([-1, 1], [-1, 1], [-1, 1])

        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])

        self.fig.subplots_adjust(
            left=0.0,
            right=1.0,
            bottom=0.0,
            top=1.0,
            wspace=0.2,
            hspace=0.2,
        )

    def draw_points(self, pc: PointCloud):
        for p in pc.positions:
            self.ax.plot(p[0], p[1], p[2], 'o', markersize=10)  # red circles
            # self.ax.plot(p.x, p.y, 'ro', markersize=10)  # red circles
        # self.ax.scatter(pc.points[:, 0], pc.points[:, 1], pc.points[:, 2],
        #     color='blue', s=10, alpha=1.0)
        plt.show()

    def draw_mesh(self, mesh: Mesh):
        m = Poly3DCollection(
            [[mesh.positions[i] for i in face] for face in mesh.faces],
            facecolors='lightblue',
            edgecolors='gray',
            linewidths=1,
            alpha=0.8
        )
        self.ax.add_collection3d(m)
        plt.show()

    def draw_normals(self, pc: PointCloud):
        pxs = [p[0] for p in pc.positions]
        pys = [p[1] for p in pc.positions]
        pzs = [p[2] for p in pc.positions]
        nxs = [n[0] for n in pc.normals]
        nys = [n[1] for n in pc.normals]
        nzs = [n[2] for n in pc.normals]
        self.ax.quiver(pxs, pys, pzs, nxs, nys, nzs,
                       length=0.15, color='green', normalize=False)

        plt.show()
