import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from model.mesh import Mesh


def draw(mesh: Mesh):
    faces = [[mesh.points[i] for i in face] for face in mesh.faces]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    m = Poly3DCollection(
        faces,
        facecolors='lightblue',
        edgecolors='gray',
        linewidths=1,
        alpha=0.8
    )
    ax.add_collection3d(m)
    # ax.auto_scale_xyz(1.0, 1.0, 1.0)
    plt.show()
