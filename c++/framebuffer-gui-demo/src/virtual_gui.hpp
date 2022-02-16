#pragma once
#include <cstdint>
#include <fstream>
#include <functional>

struct Point {
  int32_t x;
  int32_t y;

  Point() : x(0), y(0) {}
  Point(int32_t _x, int32_t _y) : x(_x), y(_y) {}
  Point(const Point &p) : x(p.x), y(p.y) {}

  friend std::ostream & operator << (std::ostream & out, const Point & p) {
    return (out << "(" << (int)p.x << ", " << (int)p.y << ")");
  }
};

struct Color {
  uint8_t r;
  uint8_t g;
  uint8_t b;

  Color() : r(0), g(0), b(0) {}
  Color(uint8_t _r, uint8_t _g, uint8_t _b) : r(_r), g(_g), b(_b) {}
  Color(const Color &c) : r(c.r), g(c.g), b(c.b) {}

  friend std::ostream & operator << (std::ostream & out, const Color & c) {
    return (out << "(" << (int)c.r << ", " << (int)c.g << ", " << (int)c.b << ")");
  }
};

class Screen {
    bool inf_loop = true;
public:
    virtual ~Screen() {}

    /* init functions */
    virtual void init_font(std::string font_name, uint16_t size) = 0;

    /* drawing functions */
    virtual void draw_pixel(const Point point, const Color color) = 0;
    virtual void draw_line(const Point p1, const Point p2, const Color color) = 0;
    virtual void draw_rect(const Point p1, const Point p2, const Color color) = 0;
    virtual void draw_rect_fill(const Point p1, const Point p2, const Color color) = 0;
    virtual void draw_text(const Point point, const Color color, const char *fmt, ...) = 0;
    virtual void clear(const Color color) = 0;
    virtual void flush() = 0;

    /* keyboard */
    virtual int get_key() = 0;

    /* other */
    const bool loop() { return inf_loop; }
    void shutdown() { inf_loop = true; }
};

class Object {
    std::function<void(Screen *, Object *)> f_on_render = nullptr;
    std::function<void(int, Object *)> f_on_key_press = nullptr;
    bool is_obj_focused = false;
public:
    virtual ~Object() {}

    void on_key_press(std::function<void(int, Object *)> f) { f_on_key_press = f; }
    void on_render(std::function<void(Screen *, Object *)> f) { f_on_render = f; }
    void key_press(int key) {
      if (f_on_key_press) {
        f_on_key_press(key, this);
      }
    }
    void render(Screen * screen) {
      if (f_on_render) {
        f_on_render(screen, this);
      }
    }

    void focus_on() { is_obj_focused = true; }
    void focus_off() { is_obj_focused = false; }
    bool is_focused() { return is_obj_focused; }
};

class View {
public:
    Screen * screen = nullptr;
    
    View() {}
    View(Screen * _screen) : screen(_screen) {}
    virtual ~View() {}

    virtual void update_state() = 0;
};