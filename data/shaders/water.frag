#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

in vec2 uv;

uniform sampler2D u_texture_0;
uniform float water_line;


void main() {
    vec3 tex_col = texture(u_texture_0, uv).rgb;
    tex_col = pow(tex_col, gamma);

    // Fog.
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    // TODO fix fog au
    //float alpha = mix(0.5, 0.0, 1.0 - exp(-0.000002 * fog_dist * fog_dist));
    //float alpha = mix(0.9, 0.0, 1.0 - exp(-0.000002 * fog_dist * fog_dist));
    tex_col = mix(tex_col, vec3(0.5, 0.67, 1), (1.0 - exp2(-0.00001 * fog_dist * fog_dist)));
    // Gamma correction.
    tex_col = pow(tex_col, inv_gamma);
    fragColor = vec4(tex_col, 0.25);
}