#include "points.hpp"

Points::Points(const uint16_t count, const float psize, const float sx, const float sy, bool randomize)
    : pixel_size(psize), sx(sx), sy(sy) {
    magic_radius = 0.6f * pixel_size;
    auto px = -sx;
    auto py = -sy;
    auto kx = 1.2f * magic_radius;
    auto ky = 1.2f * magic_radius;
    ssx = sx + 0.1f;
    ssy = sy + 0.1f;
    width = ssy / grid_size;

    position.reserve(count);
    deltaPos.reserve(count);
    acceleration.reserve(count);

    for (uint16_t i = 0; i < count; i++) {
        if (randomize) {
            auto rx = (rand() % 100 - 50) / 10000.0f;
            auto ry = (rand() % 100 - 50) / 10000.0f;
            position.push_back({px + rx, py + ry});
        } else {
            position.push_back({px, py});
        }
        deltaPos.push_back({0.0f, 0.0f});
        acceleration.push_back({0.0f, -10.0f});
        if (sx - px < delta) {
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

inline glm::vec2 Points::speed_limit(glm::vec2 a) {
    auto speed = std::abs(glm::length(a));
    if (speed < limit_speed) {
        return a;
    }
    auto k = limit_speed / speed;
    return a * k;
}

inline void Points::collide(int i, int j) {
    auto delta = position[j] - position[i];
    auto r = glm::length(delta);
    if (r < magic_radius) {
        glm::vec2 n = glm::normalize(delta);
        float depth = magic_radius - r;
        push(i, -n * depth * 0.5f);
        push(j, n * depth * 0.5f);
        glm::vec2 rel_vel = deltaPos[i] - deltaPos[j];
        float exchange_vel = (1.0f + bounce) * glm::dot(rel_vel, n);
        if (exchange_vel > 0) {
            auto f = speed_limit(n * exchange_vel * k);
            deltaPos[i] += f;
            deltaPos[j] -= f;
        }
    }
}

inline void Points::move(int i, float dt) {
    // перемещение частиый
    deltaPos[i] += acceleration[i] * dt * dt;
    position[i] += deltaPos[i];
    // - отталкивание от фиксированных границ
    glm::vec2 delta = {0, 0};
    if (position[i].x > sx) {
        delta.x = (sx - position[i].x);
    }
    if (position[i].x < -sx) {
        delta.x = (-sx - position[i].x);
    }
    if (position[i].y < -sy) {
        delta.y = (-sy - position[i].y);
    }
    if (position[i].y > sy) {
        delta.y = (sy - position[i].y);
    }
    // выталкивае частицу по delta вектору
    push(i, delta);
}

void Points::step(const float dt, bool old = false) {
    if (old) {
        // старый метод расчёта взаимодествий
        for (auto i = 0; i < position.size(); i++) {
            for (auto j = i + 1; j < position.size(); j++) {
                collide(i, j);
            }
            move(i, dt);
        }
    } else {
        // новый метод
        grid.clear();
        for (auto i = 0; i < position.size(); i++) {
            auto indexes = get_indexes(i);
            for (auto &index : indexes) {
                if (grid.find(index) != grid.end()) {
                    grid[index].insert(i);
                } else {
                    grid[index] = {i};
                }
            }
        }

        for (auto &block : grid) {
            for (auto i = block.second.begin(); i != block.second.end(); i++) {
                // TODO: rewrite this
                for (auto j = i; j != block.second.end(); j++) {
                    if (i != j) {
                        collide(*i, *j);
                    }
                }
            }
        }

        for (auto i = 0; i < position.size(); i++) {
            move(i, dt);
        }
    }
}

inline std::set<int> Points::get_indexes(int i) {
    std::vector<glm::vec2> positions = {
        // 1-----2
        // ---3---
        // 4-----5
        position[i] + glm::vec2(-magic_radius, -magic_radius),
        position[i] + glm::vec2(magic_radius, -magic_radius),
        position[i],
        position[i] + glm::vec2(-magic_radius, magic_radius),
        position[i] + glm::vec2(magic_radius, magic_radius),
    };
    std::set<int> indexes;
    for (auto &p : positions) {
        indexes.insert(index(i, p));
    }
    return indexes;
}

inline int Points::index(int i, glm::vec2 p) { return ((ssy + p.y) * width + (ssx + p.x)) / grid_size; }

inline void Points::push(int index, glm::vec2 delta) {
    position[index] += delta;
    deltaPos[index] += delta;
}

void Points::explode(glm::vec2 pos, GLfloat size, GLfloat k) {
    for (int i = 0; i < position.size(); i++) {
        glm::vec2 delta = position[i] - pos;
        glm::vec2 n = glm::normalize(delta);
        auto r = glm::length(delta);
        if (r < size) {
            push(i, n / (k * r));
        }
    }
}