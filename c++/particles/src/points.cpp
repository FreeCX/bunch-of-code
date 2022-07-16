#include "points.hpp"

Points::Points(const uint16_t count1, const uint16_t count2, const float phys_size, const float sx, const float sy)
    : sx(sx), sy(sy), count(count1 + count2), count1(count1), count2(count2) {
    auto px = -sx;
    auto py = sy;
    auto kx = 1.2f * phys_size;
    auto ky = -1.2f * phys_size;
    ssx = sx + 0.1f;
    ssy = sy + 0.1f;
    width = ssy / grid_size;

    position = new glm::vec3[count];
    delta_pos = new glm::vec2[count];
    acceleration = new glm::vec2[count];
    movable = new bool[count];

    for (uint16_t i = 0; i < count1; i++) {
        position[i] = {px, py, phys_size};
        delta_pos[i] = {0.0f, 0.0f};
        movable[i] = true;
        if (sx - px < delta) {
            py += ky * 0.8;
            px = -sx;
        } else {
            px += kx * 0.8;
        }
    }

    py += 10 * ky;
    px = -sx;
    bool shift = false;

    for (uint16_t i = count1; i < count; i++) {
        position[i] = {px, py, 4.0 * phys_size};
        delta_pos[i] = {0.0f, 0.0f};
        movable[i] = false;
        if (sx - px < 4 * delta) {
            shift = !shift;
            px = -sx + (shift ? 4.0 * kx : 0.0f);
            py += 7 * ky;
        } else {
            px += kx * 7;
        }
    }
}

Points::~Points() {
    delete[] acceleration;
    delete[] delta_pos;
    delete[] position;
    delete[] movable;
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
    auto delta = position[j].xy() - position[i].xy();
    auto r = glm::length(delta);
    auto magic_radius = 0.5f * (position[i].z + position[j].z);
    if (r < magic_radius) {
        glm::vec2 n = glm::normalize(delta);
        float depth = magic_radius - r;
        glm::vec2 v = n * depth * 0.5f;

        // часть скорости теряется на взаимодействие с недвижимым объектом
        if (not movable[i] or not movable[j]) {
            v *= 0.5f;
        }

        // толкаем частицы
        if (movable[i]) {
            push(i, -v);
        }
        if (movable[j]) {
            push(j, v);
        }

        glm::vec2 rel_vel = delta_pos[i] - delta_pos[j];
        float exchange_vel = (1.0f + bounce) * glm::dot(rel_vel, n);
        if (exchange_vel > 0) {
            auto f = speed_limit(n * exchange_vel * k);

            // часть скорости теряется на взаимодействие с недвижимым объектом
            if (not movable[i] or not movable[j]) {
                f *= 0.5f;
            }

            if (movable[i]) {
                delta_pos[i] += f;
            }
            if (movable[j]) {
                delta_pos[j] -= f;
            }
        }
    }
}

inline void Points::move(int i, float dt) {
    // перемещение частиц
    if (movable[i]) {
        delta_pos[i] += acc * dt * dt;
        position[i].x += delta_pos[i].x;
        position[i].y += delta_pos[i].y;
    }
    // - отталкивание от фиксированных границ с потерей половины скорости
    glm::vec2 delta = {0, 0};
    if (position[i].x > sx) {
        delta.x = (sx - position[i].x) * 0.5f;
    }
    if (position[i].x < -sx) {
        delta.x = (-sx - position[i].x) * 0.5f;
    }
    if (position[i].y < -sy) {
        delta.y = (-sy - position[i].y) * 0.5f;
    }
    if (position[i].y > sy) {
        delta.y = (sy - position[i].y) * 0.5f;
    }
    // выталкиваем частицу по delta вектору
    push(i, delta);
}

void Points::step(const float dt) {
    grid.clear();
    for (auto i = 0; i < count; i++) {
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
        for (auto i = block.second.cbegin(); i != block.second.cend(); i++) {
            auto j = i;
            ++j;
            for (; j != block.second.cend(); j++) {
                collide(*i, *j);
            }
        }
    }

    for (auto i = 0; i < count; i++) {
        move(i, dt);
    }
}

inline hashset Points::get_indexes(int i) {
    glm::vec2 positions[4] = {
        // 1---2
        // 3---4
        position[i].xy() + glm::vec2(-position[i].z, -position[i].z),
        position[i].xy() + glm::vec2(position[i].z, -position[i].z),
        position[i].xy() + glm::vec2(-position[i].z, position[i].z),
        position[i].xy() + glm::vec2(position[i].z, position[i].z),
    };
    hashset indexes;
    for (auto &p : positions) {
        indexes.insert(index(i, p));
    }
    return indexes;
}

inline int Points::index(int i, glm::vec2 p) { return ((ssy + p.y) * width + (ssx + p.x)) / grid_size; }

inline void Points::push(int index, glm::vec2 delta) {
    position[index].x += delta.x;
    position[index].y += delta.y;
    delta_pos[index] += delta;
}

void Points::explode(glm::vec2 pos, GLfloat size, GLfloat k) {
    for (int i = 0; i < count1; i++) {
        glm::vec2 delta = position[i].xy() - pos;
        glm::vec2 n = glm::normalize(delta);
        auto r = glm::length(delta);
        if (r < eps) {
            continue;
        }
        if (r < size) {
            push(i, k * n / r);
        }

    }
}
