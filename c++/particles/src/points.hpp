#pragma once
#include <vector>
#include <GL/gl.h>
#include <glm/geometric.hpp>
#include <glm/vec2.hpp>
#include <cmath>

struct Points {
    std::vector<glm::vec2> position;
    std::vector<glm::vec2> deltaPos;
    std::vector<glm::vec2> acceleration;
    GLfloat PIXEL_SIZE, SX, SY;

    Points(const uint16_t, const GLfloat, const GLfloat, const GLfloat);
    ~Points();
    void step(const GLfloat);
    std::vector<GLfloat> convert();
    inline void push(int index, glm::vec2 delta);
};