#include <array>
#include <vector>

#include "font.hpp"
#include "points.hpp"
#include "shader.hpp"
#include "vertex.hpp"
#include "window.hpp"

const float pixel_size = 5.0f;
const float scale_size = 12.0f * 15.0f;
const float point_size = pixel_size / scale_size;
const float phys_box_size = 0.9f;

const int grid_count = 20;
const uint16_t w_width = 800;
const uint16_t w_height = 800;
const uint16_t max_frame_skip = 5;
const uint16_t particle_count = 3000;
const char *method[] = {"grid", "n^2"};

ShaderProgram base_shader;
ShaderProgram point_shader;
Vertex data;
Vertex point;
Font font(w_width, w_height);

glm::vec4 grid_color = {1.0f, 1.0f, 1.0f, 0.2f};

Points points(particle_count, point_size, phys_box_size, phys_box_size, false);
std::array<glm::vec3, particle_count> colors;

bool pause_flag = false;
bool old_method = false;

std::vector<GLfloat> generate_grid(GLuint vlines, GLuint hlines, float r) {
    const uint32_t ncoords = 4;
    const uint32_t elements_count = ncoords * (vlines + hlines);
    const float vgrid_step = 2.0 * r / ((float)hlines - 1.0);
    const float hgrid_step = 2.0 * r / ((float)vlines - 1.0);
    std::vector<GLfloat> grid_data;

    grid_data.resize(elements_count);

    for (uint32_t i = 0; i < vlines; ++i) {
        // vertical lines
        grid_data[i * ncoords + 0] = -r + hgrid_step * i;
        grid_data[i * ncoords + 1] = -r;
        grid_data[i * ncoords + 2] = -r + hgrid_step * i;
        grid_data[i * ncoords + 3] = r;
    }
    uint32_t first_part = vlines * ncoords;
    for (uint32_t i = 0; i < hlines; ++i) {
        // horizontal lines
        grid_data[first_part + i * ncoords + 0] = -r;
        grid_data[first_part + i * ncoords + 1] = -r + vgrid_step * i;
        grid_data[first_part + i * ncoords + 2] = r;
        grid_data[first_part + i * ncoords + 3] = -r + vgrid_step * i;
    }

    return grid_data;
}

glm::vec3 hsv2rgb(glm::vec3 hsv) {
    float fC = hsv.z * hsv.y;
    float fHPrime = fmod(hsv.x / 60.0, 6);
    float fX = fC * (1 - fabs(fmod(fHPrime, 2) - 1));
    float fM = hsv.z - fC;
    glm::vec3 rgb = {0, 0, 0};

    if (0 <= fHPrime && fHPrime < 1) {
        rgb = {fC, fX, 0};
    } else if (1 <= fHPrime && fHPrime < 2) {
        rgb = {fX, fC, 0};
    } else if (2 <= fHPrime && fHPrime < 3) {
        rgb = {0, fC, fX};
    } else if (3 <= fHPrime && fHPrime < 4) {
        rgb = {0, fX, fC};
    } else if (4 <= fHPrime && fHPrime < 5) {
        rgb = {fX, 0, fC};
    } else if (5 <= fHPrime && fHPrime < 6) {
        rgb = {fC, 0, fX};
    }

    return rgb + glm::vec3(fM, fM, fM);
}

void init(void) {
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);

    base_shader.create();
    base_shader.addShader("assets/base_vertex.glsl", GL_VERTEX_SHADER);
    base_shader.addShader("assets/base_fragment.glsl", GL_FRAGMENT_SHADER);
    base_shader.link();

    point_shader.create();
    point_shader.addShader("assets/point_vertex.glsl", GL_VERTEX_SHADER);
    point_shader.addShader("assets/point_fragment.glsl", GL_FRAGMENT_SHADER);
    point_shader.link();

    auto grid = generate_grid(grid_count, grid_count, 1);
    data.load_vertex((GLfloat *)grid.data(), nullptr, 2, 0, grid.size() / 2);

    font.shader("assets/text_vertex.glsl", "assets/text_fragment.glsl");
    font.load("assets/FiraSans-Medium.ttf", 18);

    // инициализируем цвета точек
    float hue = 0.0f;
    float step = 360.0f / particle_count;
    for (int i = 0; i < particle_count; i++) {
        colors[i] = hsv2rgb(glm::vec3(hue, 1, 1));
        hue += step;
    }

    // инициализируем буферы OpenGL
    auto p = points.points();
    point.load_vertex((GLfloat *)p, (GLfloat *)colors.data(), 2, 3, particle_count, true);
}

void deinit() {}

void render(Window *window) {
    static float current_fps = 0.0f;
    static float current_user_time = 0.0f;
    static uint16_t frame_skip = 0;

    if (frame_skip-- == 0) {
        current_fps = window->get_fps();
        current_user_time = window->get_user_time();
        frame_skip = max_frame_skip;
    }

    glClear(GL_COLOR_BUFFER_BIT);
    glEnable(GL_ALPHA_TEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    // отрисовка сцены
    base_shader.run();
    base_shader.uniform("in_color", grid_color);
    data.render(GL_LINES);

    // отрисовка точек
    point_shader.run();

    // лучше так не делать
    glPointSize(pixel_size);
    // обновление положений частиц в буфере OpenGL и рендеринг
    auto p = points.points();
    point.update((GLfloat *)p);
    point.render(GL_POINTS);

    char buff[96];
    sprintf(buff, "particles: %d; method: %s; fps: %.0f; phys: %.2f ms", particle_count, method[old_method],
            current_fps, current_user_time);
    font.render(buff, glm::vec3(10.0f, 10.0f, 0.0f), glm::vec3(1.0f, 1.0f, 1.0f));

    glDisable(GL_BLEND);
    glDisable(GL_ALPHA_TEST);
}

void loop(const float fps) {
    if (!pause_flag) {
        points.step(1E-3, old_method);
    }
}

void keyboard(GLFWwindow *window, int key, int scancode, int action, int mods) {
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
        glfwSetWindowShouldClose(window, true);
    }
    if (key == GLFW_KEY_SPACE && action == GLFW_PRESS) {
        pause_flag = !pause_flag;
    }
    if (key == GLFW_KEY_M && action == GLFW_PRESS) {
        old_method = !old_method;
    }
}

void mouse(GLFWwindow *window, int button, int action, int mods) {
    const GLfloat k = 2000.0f;
    const GLfloat s = 0.2f;

    if (button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS) {
        double xpos, ypos;
        glfwGetCursorPos(window, &xpos, &ypos);
        glm::vec2 pos = {(2 * xpos - w_width) / w_width, -(2 * ypos - w_height) / w_height};
        points.explode(pos, s, k);
    }
}

int main() {
    Window window;

    window.init_window("Particles Demo", w_width, w_height);
    window.init_gl(init);
    window.render(render);
    window.keyboard(keyboard);
    window.mouse(mouse);
    window.user(loop);
    window.loop(60.0f);

    deinit();

    return 0;
}
