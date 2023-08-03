#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_color;

out vec3 color;
out vec2 uv;
const vec2 uv_coords[4] = vec2[4](
    vec2(1, 0), vec2(0, 0),
    vec2(1, 1), vec2(0, 1)
);

const int uv_indices[6] = int[6](
    1, 0, 2, 1, 2, 3
);

void main() {
    color = in_color;
    int uv_index = gl_VertexID % 6;
    uv = uv_coords[uv_indices[uv_index]];
    // No other matrices needed. Since this is in 2D, we can just use screen co-ordinates.
    gl_Position = vec4(in_position, 1.0);
}
