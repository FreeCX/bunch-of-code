#pragma once
// GLEW
#define GLEW_STATIC
#include "error.hpp"
#include <GL/glew.h>
#include <vector>

class Vertex {
  public:
    void load_vertex(const GLfloat *v, const GLfloat *c, const GLint v_size, const GLint c_size, const GLint count);
    void render(const GLuint type);

  private:
    GLuint vbo_handles[2];
    GLuint vao_handles;
    GLuint _count;
};