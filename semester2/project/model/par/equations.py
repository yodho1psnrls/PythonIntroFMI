# import numpy as np
import glm
from math import sin
from math import cos
from math import exp
from math import pi


def sphere(uv: glm.vec2):
    u = 2 * pi * uv[0]
    v = 2 * pi * uv[1]
    return glm.vec3(
        sin(u)*cos(v),
        sin(u)*sin(v),
        cos(u),
    )


def cone(uv: glm.vec2):
    u = 2 * pi * uv[0]
    v = uv[1]
    return glm.vec3([
        (1.0 - v) * cos(u),
        (1.0 - v) * sin(u),
        v
    ])


# https://math.libretexts.org/Bookshelves/Calculus/Supplemental_Modules_(Calculus)/Vector_Calculus/2%3A_Vector-Valued_Functions_and_Motion_in_Space/2.7%3A_Parametric_Surfaces
def fold_paper(uv: glm.vec2):
    u = 2 * pi * uv[0]
    v = 2 * pi * uv[1]
    return glm.vec3([
        sin(u),
        cos(v),
        exp(2*u**(1/3) + 2*v**(1/3))
    ])


def hour_glass(uv: glm.vec2):
    u = 2.0 * pi * uv[0]
    v = 2.0 * pi * uv[1]
    return glm.vec3([
        cos(u)*cos(v),
        cos(u)*sin(v),
        uv[0],  # u
    ])


def screw(uv: glm.vec2):
    u = 2.0 * pi * uv[0]
    v = 2.0 * pi * uv[1]
    return glm.vec3([
        cos(u)*cos(v),
        cos(u)*sin(v),
        uv[1],  # v
    ])

# ----------------------------------------------------------------- #

# https://www.reddit.com/r/threejs/comments/1jb12bm/a_gallery_of_parametric_surfaces_with_their/


