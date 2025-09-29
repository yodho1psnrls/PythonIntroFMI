# import glfw
import OpenGL.GL as GL


def compile_shader(src, shader_type):
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, src)
    GL.glCompileShader(shader)

    if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
        log = GL.glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compile error:\n{log}")
    return shader


class Shader:
    def __init__(self, vert_path: str, frag_path):
        if vert_path[-5:] != '.vert':
            raise RuntimeError('vertex shader file type should be .vert')
        if frag_path[-5:] != '.frag':
            raise RuntimeError('fragment shader file type should be .frag')

        with open(vert_path, 'r') as f:
            vs = compile_shader(f.read(), GL.GL_VERTEX_SHADER)
        with open(frag_path, 'r') as f:
            fs = compile_shader(f.read(), GL.GL_FRAGMENT_SHADER)

        self.program = GL.glCreateProgram()
        GL.glAttachShader(self.program, vs)
        GL.glAttachShader(self.program, fs)
        GL.glLinkProgram(self.program)

        # Delete the shaders, as they are now linked into the program
        GL.glDeleteShader(vs)
        GL.glDeleteShader(fs)

    def use(self):
        GL.glUseProgram(self.program)
