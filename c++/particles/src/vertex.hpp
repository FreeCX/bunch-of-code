#pragma once
#include <vector>

#define GLEW_STATIC
#include <GL/glew.h>

#include "error.hpp"

class Vertex {
  public:
    ~Vertex();

    void load_vertex(const GLfloat *v,
                     const GLfloat *c,
                     const GLint v_size,
                     const GLint c_size,
                     const GLint count,
                     bool dynamic = false);
    void update(const GLfloat *v);
    void render(const GLuint type);

  private:
    GLuint vbo_handles[2];
    GLuint vao_handles;
    GLuint _buffers;
    GLuint _vsize;
    GLuint _csize;
    GLuint _count;
};
