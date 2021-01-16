#pragma once
#include <cmath>
#include <GL/gl.h>
#include <glm/geometric.hpp>
#include <glm/vec2.hpp>
#include <vector>
#include <map>
#include <set>

class Points {
    const float bounce = 0.5f;
    const float k = 0.01f;
    const float delta = 0.05f;
    const float limit_speed = 1E-1;
    const float grid_size = 0.2f;

    std::map<int, std::set<int>> grid;

    std::vector<glm::vec2> position;
    std::vector<glm::vec2> deltaPos;
    std::vector<glm::vec2> acceleration;
    float magic_radius, pixel_size, sx, sy;
    float width, ssx, ssy;

    inline glm::vec2 speed_limit(glm::vec2 a);
    inline void collide(int i, int j);
    inline void move(int i, float dt);
    inline void push(int index, glm::vec2 delta);
    inline int index(int i, glm::vec2 p);
    inline std::set<int> get_indexes(int i);
public:
    Points(const uint16_t, const float, const float, const float);
    ~Points();
    void step(const float, bool);
    std::vector<GLfloat> convert();
};