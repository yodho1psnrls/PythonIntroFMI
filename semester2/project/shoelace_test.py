from model.mesh import Mesh
from model.vertex import Vertex
import glm

if __name__ == '__main__':
    square = Mesh(
        [
            Vertex(glm.vec3(0.0, 0.0, 10.0)),
            Vertex(glm.vec3(1.0, 0.0, 10.0)),
            Vertex(glm.vec3(1.0, 1.0, 10.0)),
            Vertex(glm.vec3(0.0, 1.0, 10.0)),
        ],
        [
            [0, 1, 2, 3]
        ]
    )
    print(square.area())    # 20
    # NOTE: Doesnt work in 3D !!!
