#version 330 core
// #version 460 core

in vec3 norm;
in vec2 uv;

out vec4 frag_color;

uniform sampler2D tex;
uniform vec3 light_dir;
uniform vec3 light_color;
uniform vec3 base_color;

void main() {
    float diff = max(dot(normalize(norm), normalize(-light_dir)), 0.0);
    vec3 tex_color = texture(tex, uv).rgb;
    vec3 final_color = base_color * tex_color * (0.2 + diff * light_color);
    frag_color = vec4(final_color, 1.0);
}
