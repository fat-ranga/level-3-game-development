#version 330 core

layout (location = 0) in uint packed_data;
//layout (location = 1) in vec2 uv_coords_fr; // I give up trying to calculate them here.

int x, y, z;
int ao_id;
int flip_id;
int texture_id;
int face_id;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;



//out vec3 voxel_color;
out vec2 uv;
out float shading;
out vec3 frag_world_pos;

const float ao_values[4] = float[4](0.1, 0.25, 0.5, 1.0);

const float face_shading[6] = float[6](
    1.0, 0.5,  // top bottom
    0.5, 0.8,  // right left
    0.5, 0.8   // front back
);

const vec2 uv_coords[4] = vec2[4](
    vec2(0, 0), vec2(0, 1),
    vec2(1, 0), vec2(1, 1)
);

//const vec2 uv_coords[4] = vec2[4](
//    vec2(1, 1), vec2(1, 0),
//    vec2(0, 1), vec2(0, 0)
//);

// We use the lower two rows of UV co-ordinates if the face is flipped.
const int uv_indices[24] = int[24](
    1, 0, 2, 1, 2, 3,  // Texture co-ordinate indices for the vertices of an even face.
    3, 0, 2, 3, 1, 0,  // Odd face.
    3, 1, 0, 3, 0, 2,  // Even flipped face.
    1, 2, 3, 1, 0, 2   // Odd flipped face.
);


vec3 hash31(float p) {
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}

// We are always working with an unsigned data type, which is why it is uint instead of int.
void unpack(uint packed_data) {
    // TODO: 8 bits for texture_id means only 256 different possible texture values.
    // a, b, c, d, e, f, g = x, y, z, texture_id, face_id, ao_id, flip_id
    uint b_bit = 6u, c_bit = 6u, d_bit = 8u, e_bit = 3u, f_bit = 2u, g_bit = 1u;
    uint b_mask = 63u, c_mask = 63u, d_mask = 255u, e_mask = 7u, f_mask = 3u, g_mask = 1u;
    //
    uint fg_bit = f_bit + g_bit;
    uint efg_bit = e_bit + fg_bit;
    uint defg_bit = d_bit + efg_bit;
    uint cdefg_bit = c_bit + defg_bit;
    uint bcdefg_bit = b_bit + cdefg_bit;
    // Unpacking vertex data.
    x = int(packed_data >> bcdefg_bit);
    y = int((packed_data >> cdefg_bit) & b_mask);
    z = int((packed_data >> defg_bit) & c_mask);
    //
    texture_id = int((packed_data >> efg_bit) & d_mask);
    face_id = int((packed_data >> fg_bit) & e_mask);
    ao_id = int((packed_data >> g_bit) & f_mask);
    flip_id = int(packed_data & g_mask);
}


void main() {
    unpack(packed_data);

    vec3 in_position = vec3(x, y, z);

    int uv_index = gl_VertexID % 6  + ((face_id & 1) + flip_id * 2) * 6;

    //uv_index += 1;

    //uv = uv_coords[uv_indices[uv_index]];
    uv = uv_coords[uv_indices[uv_index]];

    float normalised_voxel_texture_size = 1.0 / 8.0;
	int current_row = int((texture_id / 8.0) + 1); // texture_id
	float uv_x = float((texture_id / 8.0) - (current_row - 1)); // texture_id
	float uv_y = float((current_row - 1) / 8.0);

    // For some reason, the x axis is flipped, so we un-flip it in this offset.
    vec2 uv_offset = vec2(1 - (uv_x + normalised_voxel_texture_size), uv_y);

    //uv += uv_offsets[uv_indices[uv_index]];

    uv /= 8.0;
    uv += uv_offset;
    //uv += uv_offsets[uv_indices[uv_index]];

    //int vertex_face_id_thing = uv_index % 6;

    //switch(vertex_face_id_thing){
    //         case 0:
    //             uv = vec2(uv_x + normalised_block_texture_size, uv_y);
    //             break;
    //         case 1:
    //             uv = vec2(uv_x + 0.0, uv_y + 0.0);
    //             break;
    //         case 2:
    //             uv = vec2(uv_x + normalised_block_texture_size, uv_y + normalised_block_texture_size);
    //             break;
    //         case 3:
    //             uv = vec2(uv_x, uv_y + normalised_block_texture_size);
    //             break;
    // }

    //uv = vec2(uv_x, uv_y);

    //uv /= 4;
   // uv += 0.1;

    shading = face_shading[face_id] * ao_values[ao_id];
    frag_world_pos = (m_model * vec4(in_position, 1.0)).xyz;

    gl_Position = m_proj * m_view * vec4(frag_world_pos, 1.0);
}
