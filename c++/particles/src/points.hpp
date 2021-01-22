#pragma once
#include <GL/gl.h>
#include <array>
#include <cmath>
#include <glm/geometric.hpp>
#include <glm/vec2.hpp>
#include <unordered_map>
#include <unordered_set>

typedef std::unordered_set<int> hashset;
typedef std::unordered_map<int, hashset> hashmap;

class Points {
    const float bounce = 0.5f;
    const float delta = 0.05f;
    const float eps = 1E-2;
    const float grid_size = 0.2f;
    const float k = 1E-2;
    const float limit_speed = 1E-1;

    float magic_radius, pixel_size, sx, sy;
    float width, ssx, ssy;
    int count;

    hashmap grid;
    glm::vec2 *position = nullptr;
    glm::vec2 *delta_pos = nullptr;
    glm::vec2 *acceleration = nullptr;

    inline glm::vec2 speed_limit(glm::vec2 a);
    inline void collide(int i, int j);
    inline void move(int i, float dt);
    inline void push(int index, glm::vec2 delta);
    inline int index(int i, glm::vec2 p);
    inline hashset get_indexes(int i);

  public:
    Points(const uint16_t, const float, const float, const float, bool);
    ~Points();
    void step(const float, bool);
    void explode(glm::vec2 pos, GLfloat s, GLfloat k);
    glm::vec2 *points() { return position; }
};