#include <vector>
#include "window.hpp"
#include "shader.hpp"
#include "vertex.hpp"
#include "font.hpp"
#include "points.hpp"

const uint16_t w_width = 600;
const uint16_t w_height = 600;
const GLfloat PIXEL_SIZE = 8.0f;
const int SIZE = 10;
const uint16_t MAX_FRAME_SKIP = 5;
const uint16_t particle_count = 500;

ShaderProgram shader;
Vertex data;
Vertex point;

Points points(particle_count, PIXEL_SIZE / (SIZE * 15), 0.9f, 0.9f);

Font font(w_width, w_height);

bool pause_flag = false;

std::vector<GLfloat> generate_grid(GLuint vlines, GLuint hlines, float r) {
    const uint32_t ncoords = 4;
    const uint32_t elements_count = ncoords * (vlines + hlines);
    const float vgrid_step = 2.0 * r / ((float) hlines - 1.0);
    const float hgrid_step = 2.0 * r / ((float) vlines - 1.0);
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

void init(void) {
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);

    shader.create();
    shader.addShader("assets/vertex.glsl", GL_VERTEX_SHADER);
    shader.addShader("assets/fragment.glsl", GL_FRAGMENT_SHADER);
    shader.link();

    auto grid = generate_grid(SIZE, SIZE, 1);
    data.load_data(grid, 2);

    font.shader("assets/vertex_text.glsl", "assets/fragment_text.glsl");
    font.load("assets/FiraSans-Medium.ttf", 18);
}

void deinit() {}

void render(Window * window) {
    static float current_fps = 0.0f;
    static float current_user_time = 0.0f;
    static uint16_t frame_skip = 0;

    if (frame_skip-- == 0) {
        current_fps = window->get_fps();
        current_user_time = window->get_user_time();
        frame_skip = MAX_FRAME_SKIP;
    } 

    glClear(GL_COLOR_BUFFER_BIT);

    shader.run();
    shader.uniform("ourColor", glm::vec4(1.0f, 1.0f, 1.0f, 0.2f));

    glEnable(GL_ALPHA_TEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    data.render(GL_LINES);

    shader.uniform("ourColor", glm::vec4(0.0f, 0.6f, 0.7f, 1.0f));

    // don't do that
    glPointSize(PIXEL_SIZE);

    point.load_data(points.convert(), 2);
    point.render(GL_POINTS);

    char buff[64];
    sprintf(buff, "fps: %.0f", current_fps);
    font.render(buff, glm::vec3(10.0f, 50.0f, 0.0f), glm::vec3(1.0f, 1.0f, 1.0f));
    sprintf(buff, "phys: %.2f ms", current_user_time);
    font.render(buff, glm::vec3(10.0f, 30.0f, 0.0f), glm::vec3(1.0f, 1.0f, 1.0f));
    sprintf(buff, "particles: %d", particle_count);
    font.render(buff, glm::vec3(10.0f, 10.0f, 0.0f), glm::vec3(1.0f, 1.0f, 1.0f));

    glDisable(GL_BLEND);
    glDisable(GL_ALPHA_TEST);
}

void loop(const float fps) {
    if (!pause_flag) {
        points.step(fps);
    }
}

void keyboard(GLFWwindow * window, int key, int scancode, int action, int mods) {
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
        glfwSetWindowShouldClose(window, true);
    }
    if (key == GLFW_KEY_SPACE && action == GLFW_PRESS) {
        pause_flag = !pause_flag;
    }
    // if (key == GLFW_KEY)
}

int main() {
    Window window;

    window.init_window("Particles Demo", w_width, w_height);
    window.init_gl(init);
    window.render(render);
    window.keyboard(keyboard);
    window.user(loop);
    window.loop(60.0f);

    deinit();

    return 0;
}