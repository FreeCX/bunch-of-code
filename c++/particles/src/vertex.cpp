#include "vertex.hpp"

Vertex::~Vertex() {
    glDeleteBuffers(_buffers, vbo_handles);
    glDeleteVertexArrays(1, &vao_handles);
}

void Vertex::load_vertex(
    const GLfloat *v, const GLfloat *c, const GLint v_size, const GLint c_size, const GLint count, bool dynamic) {
    _count = count;
    _vsize = v_size;
    _buffers = (c == nullptr) ? 1 : 2;
    auto draw_type = dynamic ? GL_STREAM_DRAW : GL_STATIC_DRAW;

    // буферы для данных
    glGenBuffers(_buffers, vbo_handles);

    // vertex
    glBindBuffer(GL_ARRAY_BUFFER, vbo_handles[0]);
    glBufferData(GL_ARRAY_BUFFER, v_size * count * sizeof(GLfloat), v, draw_type);

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

void Vertex::update(const GLfloat *v) {
    glBindBuffer(GL_ARRAY_BUFFER, vbo_handles[0]);
    glBufferSubData(GL_ARRAY_BUFFER, 0, _vsize * _count * sizeof(GLfloat), v);
}

void Vertex::render(const GLuint type) {
    glBindVertexArray(vao_handles);
    glDrawArrays(type, 0, _count);
}