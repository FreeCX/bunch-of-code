#pragma once
#include <chrono>
#include <cmath>
#include <stdint.h>
#include <string>
#include <thread>
//
// GLEW
#define GLEW_STATIC
#include <GL/glew.h>
// GLFW
#include <GLFW/glfw3.h>
// ...
#include "error.hpp"

class Window {
public:
    void init_window(const char * caption, uint16_t width, uint16_t height);
    void loop(float fps);
    void render(void (*rend_func)(Window * window));
    void init_gl(void (*init_func)(void));
    void keyboard(void (*keyboard_func)(GLFWwindow *, int, int, int, int));
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
    GLFWwindow * window = nullptr;
    void (*render_callback)(Window *);
    void (*user_callback)(const GLfloat);
    void (*init_callback)(void);
    void (*keyboard_callback)(GLFWwindow *, int, int, int, int);
};