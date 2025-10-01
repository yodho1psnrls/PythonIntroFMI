import OpenGL.GL as GL
from gen.mesh import Mesh


# A Mesh, but loaded into the GPU
class Renderable:
    def __init__(self, mesh: Mesh):
        if not mesh.is_triangulated():
            raise RuntimeError("The mesh should be triangulated before loading into the GPU")
        self.index_count = len(mesh.faces) * 3
        self.VAO = GL.glGenVertexArrays(1)
        self.VBO = GL.glGenBuffers(1)
        self.EBO = GL.glGenBuffers(1)

        GL.glBindVertexArray(self.VAO)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, mesh.points.nbytes, mesh.points, GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, mesh.faces.nbytes, mesh.faces, GL.GL_STATIC_DRAW)

        stride = mesh.points.strides[0]

        # position (location = 0)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, GL.ctypes.c_void_p(mesh.points.dtype.fields['pos'][1]))

        # normal (location = 1)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, GL.ctypes.c_void_p(mesh.points.dtype.fields['norm'][1]))

        # uv (location = 2)
        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, GL.ctypes.c_void_p(mesh.points.dtype.fields['uv'][1]))

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

    def draw(self):
        GL.glBindVertexArray(self.VAO)
        GL.glDrawElements(GL.GL_TRIANGLES, self.index_count, GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.VAO])
        GL.glDeleteBuffers(1, [self.VBO])
        GL.glDeleteBuffers(1, [self.EBO])
