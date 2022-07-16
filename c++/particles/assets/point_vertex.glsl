#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;

uniform float scale_size;

out vec3 point_color;

void main() {
    point_color = color;
    gl_Position = vec4(position.xy, 0.0, 1.0);
    gl_PointSize = position.z * scale_size;
}
