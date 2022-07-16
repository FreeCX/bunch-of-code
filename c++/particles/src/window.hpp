#pragma once
#include <chrono>
#include <cmath>
#include <cstdint>
#include <string>
#include <thread>

#define GLEW_STATIC
#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include "error.hpp"

class Window {
  public:
    void init_window(const char *caption, uint16_t width, uint16_t height);
    void loop(float fps);
    void render(void (*rend_func)(Window *window));
    void init_gl(void (*init_func)(void));
    void keyboard(void (*keyboard_func)(GLFWwindow *, int, int, int, int));
    void mouse(void (*mouse_func)(GLFWwindow *, int, int, int));
    void user(void (*user_func)(const GLfloat));
    float get_fps();
    float get_user_time();

  private:
    void window_sleep();

    void render_main_thread();
    void user_main_thread();

    float fps;
    float real_fps;
    float user_time;
    uint16_t w_width;
    uint16_t w_height;
    GLFWwindow *window = nullptr;
    void (*render_callback)(Window *) = nullptr;
    void (*user_callback)(const GLfloat) = nullptr;
    void (*init_callback)(void) = nullptr;
    void (*keyboard_callback)(GLFWwindow *, int, int, int, int) = nullptr;
    void (*mouse_callback)(GLFWwindow *, int, int, int) = nullptr;
};
