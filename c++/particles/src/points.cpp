#include "points.hpp"
#include <iostream>

const GLfloat DELTA = 0.05f;
const GLfloat LIMIT_SPEED = 1E-1;

Points::Points(const uint16_t count, const GLfloat psize, const GLfloat sx, const GLfloat sy) {
    PIXEL_SIZE = psize; SX = sx; SY = sy;
    auto px = -sx;
    auto py = -sy;
    auto kx = 2.0f * sx / std::sqrt(count);
    auto ky = 2.0f * sy / std::sqrt(count);
    position.reserve(count);
    deltaPos.reserve(count);
    acceleration.reserve(count);
    for (uint16_t i = 0; i < count; i++) {
        auto rx = (rand() % 100 - 50) / 10000.0f;
        auto ry = (rand() % 100 - 50) / 10000.0f;
        position.push_back({ px + rx, py + ry });
        deltaPos.push_back({ 0.0f, 0.0f });
        acceleration.push_back({ 0.0f, -10.0f });
        if (sx - px < DELTA) {
            py += ky;
            px = -sx;
        } else {
            px += kx;
        }
    }
}

Points::~Points() {
    position.clear();
    deltaPos.clear();
    acceleration.clear();
}

inline glm::vec2 speed_limit(glm::vec2 a) {
    auto speed = std::abs(glm::length(a));
    if (speed < LIMIT_SPEED) {
        return a;
    }
    auto k = LIMIT_SPEED / speed;
    return a * k;
}

void Points::step(const GLfloat fps) {
    // расстоянием между двумя шариками
    const float MAGIC_RADIUS = 0.6f * PIXEL_SIZE;
    // коэффициент отскока [0, 1]
    const float bounce = 0.5f;
    const float dt = 0.002f;
    const float k = 0.05f;
    for (auto i = 0; i < position.size(); i++) {
        for (auto j = i + 1; j < position.size(); j++) {
            auto delta = position[j] - position[i];
            auto r = glm::length(delta);
            if (r < MAGIC_RADIUS) {
                glm::vec2 n = glm::normalize(delta);
                float depth = MAGIC_RADIUS - r;
                push(i, -n * depth * 0.5f);
                push(j,  n * depth * 0.5f);
                glm::vec2 rel_vel = deltaPos[i] - deltaPos[j];
                float exchange_vel = (1.0f + bounce) * glm::dot(rel_vel, n);
                if (exchange_vel > 0) {
                    auto f = speed_limit(n * exchange_vel * k);
                    deltaPos[i] += f;
                    deltaPos[j] -= f;
                }
            }
        }
        deltaPos[i] += acceleration[i] * dt * dt;
        position[i] += deltaPos[i];
        // используем строгий порядок расчёта:
        // - взаимодействие частиц
        // - расчёт перемещения частицы
        // - отталкивание от фиксированных границ
        glm::vec2 delta = {0, 0};
        if (position[i].x > SX) {
            delta.x = (SX - position[i].x);
        }
        if (position[i].x < -SX) {
            delta.x = (-SX - position[i].x);
        }
        if (position[i].y < -SY) {
            delta.y = (-SY - position[i].y);
        }
        if (position[i].y > SY) {
            delta.y = (SY - position[i].y);
        }
        push(i, delta);
    }
}

inline void Points::push(int index, glm::vec2 delta) {
    position[index] += delta;
    deltaPos[index] += delta;
}

std::vector<GLfloat> Points::convert() {
    std::vector<GLfloat> res;
    for (auto item : position) {
        res.push_back(item.x);
        res.push_back(item.y);
    }
    return res;
}
