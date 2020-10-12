#pragma once
// GLEW
#define GLEW_STATIC
#include <GL/glew.h>
#include "error.hpp"
#include <vector>

class Vertex {
public:
    void load_data(const std::vector<GLfloat> vertex, const GLint size, const GLsizei strides);
    void load_data(const std::vector<GLfloat> vertex, const GLint size);
    void load_data(const GLfloat * start, const GLfloat * end, const GLint size, const GLsizei strides);
    void load_data(const GLfloat * start, const GLfloat * end, const GLint size);
    void render(const GLuint type);
private:
    GLuint _vert_size;
    GLuint _size_count;
    GLuint _stride_count;
    GLuint VBO;
    GLuint VAO;
};