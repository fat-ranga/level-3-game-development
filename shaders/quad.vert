#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_color;

out vec3 color;

void main(){
	color = in_color;
	// Vector 4 because matrices need to be multiplied, a 3D translation is also a 4D shear.
	gl_Position = vec4(in_position, 1.0);
}