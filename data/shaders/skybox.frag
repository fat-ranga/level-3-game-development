#version 330 core
out vec4 fragColor;

in vec3 texCubeCoords;

uniform samplerCube u_texture_skybox;


void main() {
    vec3 tex_col = texture(u_texture_skybox, texCubeCoords).rgb;

    fragColor = vec4(tex_col, 1);
}