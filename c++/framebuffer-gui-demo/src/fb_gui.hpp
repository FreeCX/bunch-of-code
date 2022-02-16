#pragma once
#include <sstream>
#include <vector>

#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <linux/fb.h>
#include <ft2build.h>
#include <stdarg.h>
#include FT_FREETYPE_H

#include "virtual_gui.hpp"

class FBScreen : public Screen {
    /* fb data */
    struct fb_var_screeninfo vinfo;
    struct fb_fix_screeninfo finfo;
    char * draw_buffer;
    char * screen_buffer;
    long int screen_size;
    int fbfd;
    uint8_t buffer_index = 0;

    /* font data */
    FT_Library library;
    FT_Face face;
    FT_GlyphSlot slot;
    const uint16_t font_dpi = 100;
    uint16_t font_size = 0;

    /* stdin */
    termios orig_term, raw_term;
public:
    FBScreen(std::string device_name);
    ~FBScreen();

    /* init functions */
    void init_font(std::string font_name, uint16_t size);

    /* drawing functions */
    void draw_pixel(const Point point, const Color color);
    void draw_line(const Point p1, const Point p2, const Color color);
    void draw_rect(const Point p1, const Point p2, const Color color);
    void draw_rect_fill(const Point p1, const Point p2, const Color color);
    void draw_text(const Point point, const Color color, const char *fmt, ...);
    void clear(const Color color);
    void flush();

    int get_key();

    void draw_line_high(Point p1, Point p2, Color color);
    void draw_line_low(Point p1, Point p2, Color color);
};

class FBView : public View {
    std::vector<Object *> objects;
    size_t curr_object = 0;
    size_t prev_object = 0;
    Color clear_color;
    FBScreen * screen = nullptr;
public:
    FBView(FBScreen * _screen) : screen(_screen) {}

    void set_bg_color(const Color color) { clear_color = color; }
    void push_object(Object * object) { objects.push_back(object); }
    void next_focus() {
        prev_object = curr_object;
        if (curr_object + 1 < objects.size()) {
            ++curr_object;
        } else {
            curr_object = 0;
        }
    }
    void update_state();
};