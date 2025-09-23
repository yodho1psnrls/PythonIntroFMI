import OpenGL.GL as GL
from model.mesh import Mesh


# A Mesh, but loaded into the GPU
class Renderable:
    def __init__(self, mesh: Mesh):
        if not mesh.is_triangulated():
            raise RuntimeError("The mesh should be triangulated before loading into the GPU")

        self.index_count = len(mesh.faces) * 3
        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)
        self.VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        # GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

        self.EBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        # GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, mesh.indices.nbytes, mesh.indices, GL.GL_STATIC_DRAW)

        # Unbind
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

    def draw(self):
        GL.glBindVertexArray(self.VAO)
        # GL.glDrawArrays(GL.GL_TRIANGLES, 0, num_vertices)
        GL.glDrawElements(GL.GL_TRIANGLES, self.index_count, GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)


