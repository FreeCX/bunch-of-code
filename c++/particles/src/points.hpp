#pragma once
#define GLM_FORCE_SWIZZLE
#include <array>
#include <cmath>
#include <unordered_map>
#include <unordered_set>

#include <GL/gl.h>
#include <glm/glm.hpp>

typedef std::unordered_set<int> hashset;
typedef std::unordered_map<int, hashset> hashmap;

class Points {
    const float bounce = 0.5f;
    const float delta = 0.01f;
    const float eps = 1E-2;
    const float grid_size = 0.2f;
    const float k = 1E-2;
    const float limit_speed = 1E-1;

    float sx, sy;
    float width, ssx, ssy;
    int count, count1, count2;

    hashmap grid;
    glm::vec2 acc = {0.0f, -10.0f};
    glm::vec3 *position = nullptr;
    glm::vec2 *delta_pos = nullptr;
    glm::vec2 *acceleration = nullptr;
    bool *movable = nullptr;

    inline glm::vec2 speed_limit(glm::vec2 a);
    inline void collide(int i, int j);
    inline void move(int i, float dt);
    inline void push(int index, glm::vec2 delta);
    inline int index(int i, glm::vec2 p);
    inline hashset get_indexes(int i);

  public:
    Points(const uint16_t, const uint16_t, const float, const float, const float);
    ~Points();
    void step(const float);
    void gravity(glm::vec2 g) { acc = g; }
    void explode(glm::vec2 pos, GLfloat s, GLfloat k);
    glm::vec3 *points() { return position; }
};
