#version 330 core
// #version 460 core

layout (location = 0) in vec3 pos;
layout (location = 1) in vec3 norm;
layout (location = 2) in vec2 uv;

out vec3 out_norm;
out vec2 out_uv;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(pos, 1.0);
    out_norm = mat3(transpose(inverse(model))) * norm;
    out_uv = uv;
}
