#include "vertex.hpp"

void Vertex::load_vertex(const GLfloat *v, const GLfloat *c, const GLint v_size, const GLint c_size, const GLint count) {
    _count = count;

    // буферы для данных
    if (c == nullptr) {
        glGenBuffers(1, vbo_handles);
    } else {
        glGenBuffers(2, vbo_handles);
    }

    // vertex
    glBindBuffer(GL_ARRAY_BUFFER, vbo_handles[0]);
    glBufferData(GL_ARRAY_BUFFER, v_size * count * sizeof(GLfloat), v, GL_STATIC_DRAW);

    if (c != nullptr) {
        // color
        glBindBuffer(GL_ARRAY_BUFFER, vbo_handles[1]);
        glBufferData(GL_ARRAY_BUFFER, c_size * count * sizeof(GLfloat), c, GL_STATIC_DRAW);
    }

    // objects data
    glGenVertexArrays(1, &vao_handles);
    glBindVertexArray(vao_handles);

    glEnableVertexAttribArray(0); // vertex
    if (c != nullptr) {
        glEnableVertexAttribArray(1); // color
    }

    // 0
    glBindBuffer(GL_ARRAY_BUFFER, vbo_handles[0]);
    glVertexAttribPointer(0, v_size, GL_FLOAT, GL_FALSE, 0, NULL);

    if (c != nullptr) {
        // 1
        glBindBuffer(GL_ARRAY_BUFFER, vbo_handles[1]);
        glVertexAttribPointer(1, c_size, GL_FLOAT, GL_FALSE, 0, NULL);   
    }
}

void Vertex::render(const GLuint type) {
    glBindVertexArray(vao_handles);
    glDrawArrays(type, 0, _count);
}