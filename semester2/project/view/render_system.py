import glfw
import OpenGL.GL as GL
# import numpy as np
from view.shader import Shader
from view.renderable import Renderable
from view.renderable import Mesh


class RenderSystem:
    def __init__(self):
        # glfw.GLFW.glCreate
        if not glfw.init():
            raise Exception("glfw init failed")
        self.window = glfw.create_window(1280, 720, "SDF Editor", None, None)
        glfw.make_context_current(self.window)
        self.shader = Shader('shaders/default.vert', 'shaders/default.frag')
        # Directly use it in the engine constructor,
        #  as we wont use other shaders
        self.shader.use()
        self.renderables = []

    def print_version(self):
        print(GL.glGetString(GL.GL_VERSION).decode())
        print(GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode())
        # 4.6.0 - Build 27.20.100.8729
        # 4.60 - Build 27.20.100.8729

    # vertices = np.array([
    #     -0.5, -0.5, 0.0,
    #     0.5, -0.5, 0.0,
    #     0.0,  0.5, 0.0
    # ], dtype=np.float32)

    def draw(self, r: Renderable):
        GL.glBindVertexArray(r.VAO)
        # GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3) # Draws the Mesh !
        pass

    def run(self):
        while not glfw.window_should_close(self.window):
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            for r in self.renderables:
                self.draw(r)
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()

    def load_mesh(self, mesh: Mesh):
        self.renderables.append(Renderable(mesh))
