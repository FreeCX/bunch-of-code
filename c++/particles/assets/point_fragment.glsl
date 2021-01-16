#version 330 core

in vec3 point_color;
out vec4 out_color;

void main() {
    out_color = vec4(point_color, 1.0);
}
