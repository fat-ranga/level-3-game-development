#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 color;
uniform sampler2D u_texture_0;
in vec2 uv;

void main() {
    vec4 tex_col = texture(u_texture_0, uv).rgba;

    fragColor = vec4(tex_col);
}
