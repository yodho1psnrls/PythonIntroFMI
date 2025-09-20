import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from model.mesh import Mesh


def draw(mesh: Mesh):
    # Convert quads to list of vertex coordinates
    # faces = [mesh.points[quad] for quad in indices]
    faces = [[mesh.points[i] for i in poly] for poly in mesh.indices]

    # Create the plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Add mesh
    mesh = Poly3DCollection(
        faces,
        facecolors='lightblue',
        edgecolors='gray',
        linewidths=1,
        alpha=0.8)
    ax.add_collection3d(mesh)

    # Auto scale axes to fit the mesh
    # scale = mesh.points.flatten()
    # ax.auto_scale_xyz(scale, scale, scale)

    plt.show()
