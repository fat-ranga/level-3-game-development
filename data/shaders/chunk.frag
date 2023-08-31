#version 330 core

layout (location = 0) out vec4 fragColor;

// These are for converting our sRGB textures into linear colour space.
const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2D atlas_texture;
uniform vec3 bg_color;
uniform float water_line;

in vec2 uv;
in float shading;
in vec3 frag_world_pos;

//flat in int face_id;
//flat in int voxel_id;


void main() {
   // vec2 face_uv = uv;
    //face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    vec3 tex_col = texture(atlas_texture, uv).rgb;
    tex_col = pow(tex_col, gamma);

    tex_col *= shading;
    vec3 water_colour = vec3(0, 0.02, 0.04);
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    float inverse_fog = 1 / fog_dist;
    // Underwater absorption.
    //if (frag_world_pos.y < water_line) tex_col *= vec3(0.0, 0.3, 1.0) * vec3(fog_dist, fog_dist, fog_dist);
    if (frag_world_pos.y < water_line) {
        tex_col = mix(tex_col, water_colour, 1.0 - exp(-0.2 * fog_dist));
    }
        //tex_col *= vec3(0.01, 0.2, 0.4) * vec3(inverse_fog, inverse_fog, inverse_fog);}
        // todo make this based on whether the player is under the water
    else{
        // Atmosphere / fog. More alpha means more blue background showing.
        tex_col = mix(tex_col, bg_color * vec3(0.3, 0.5, 0.85), (1.0 - exp2(-0.00001 * fog_dist * fog_dist)));}

    tex_col = pow(tex_col, inv_gamma);
    fragColor = vec4(tex_col, 1.0);
}
