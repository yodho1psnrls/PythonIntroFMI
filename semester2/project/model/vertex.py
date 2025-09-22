import glm


class Vertex:
    def __init__(
        self,
        pos: glm.vec3 = glm.vec3(),
        norm: glm.vec3 = glm.vec3(),
        uv: glm.vec2 = glm.vec2()
    ):
        self.pos = pos      # position
        self.norm = norm    # surface normal (points up from the surface)
        self.uv = uv        # uv texture coordinates (from (0, 0) to (1, 1))

    def __hash__(self):
        return hash(self.pos) ^ (hash(self.norm) << 1) ^ (hash(self.uv) << 2)

    def __add__(self, other):
        result = Vertex()
        result.pos = self.pos + other.pos
        result.norm = self.norm + other.norm
        result.uv = self.uv + other.uv
        return result

    def __sub__(self, other):
        result = Vertex()
        result.pos = self.pos - other.pos
        result.norm = self.norm - other.norm
        result.uv = self.uv - other.uv
        return result

    def __mul__(self, scalar: float):
        return Vertex(
            self.pos * scalar,
            self.norm * scalar,
            self.uv * scalar,
        )

    def __rmul__(self, scalar: float):
        return Vertex(
            scalar * self.pos,
            scalar * self.norm,
            scalar * self.uv,
        )

    def eq(self, other) -> bool:
        return self.pos == other.pos and self.norm == other.norm and self.uv == other.uv
