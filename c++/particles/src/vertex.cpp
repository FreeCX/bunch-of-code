#include "vertex.hpp"

void Vertex::load_data(const std::vector<GLfloat> vertex, const GLint size, const GLsizei strides) {
    load_data(vertex.data(), vertex.data() + vertex.size(), size, strides);
}

void Vertex::load_data(const std::vector<GLfloat> vertex, const GLint size) {
    load_data(vertex.data(), vertex.data() + vertex.size(), size, size);
}

void Vertex::load_data(const GLfloat * start, const GLfloat * end, const GLint size, const GLsizei strides) {
    _size_count = size;
    _stride_count = strides;
    _vert_size = end - start;

    glGenBuffers(1, &VBO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, _vert_size * sizeof(GLfloat), start, GL_STATIC_DRAW);
    glVertexAttribPointer(0, size, GL_FLOAT, GL_FALSE, strides * sizeof(GLfloat), (GLvoid *)0);

    glEnableVertexAttribArray(0);

    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, _vert_size * sizeof(GLfloat), start, GL_STATIC_DRAW);
    glVertexAttribPointer(0, size, GL_FLOAT, GL_FALSE, strides * sizeof(GLfloat), (GLvoid *)0);
    glEnableVertexAttribArray(0);
    glBindVertexArray(0);
}

void Vertex::load_data(const GLfloat * start, const GLfloat * end, const GLint size) {
    load_data(start, end, size, size);
}

void Vertex::render(const GLuint type) {
    glBindVertexArray(VAO);
    glDrawArrays(type, 0, _vert_size / _size_count);
    glBindVertexArray(0);
}