#include "fb_gui.hpp"

FBScreen::FBScreen(std::string device_name) {
    /* init fb */
    fbfd = open(device_name.c_str(), O_RDWR);
    if (fbfd == -1) {
        throw std::runtime_error("cannot open framebuffer device");
    }
    if (ioctl(fbfd, FBIOGET_FSCREENINFO, &finfo) == -1) {
        throw std::runtime_error("error reading fixed information");
    }
    if (ioctl(fbfd, FBIOGET_VSCREENINFO, &vinfo) == -1) {
        throw std::runtime_error("error reading variable information");
    }
    screen_size = vinfo.xres * vinfo.yres * vinfo.bits_per_pixel / 8;
    screen_buffer = (char *)mmap(0, screen_size, PROT_READ | PROT_WRITE, MAP_SHARED, fbfd, 0);
    if (*(int *)screen_buffer == -1) {
        throw std::runtime_error("failed to map framebuffer device to memory");
    }
    draw_buffer = new char [screen_size];

    /* set stdin */
    tcgetattr(STDIN_FILENO, &orig_term);
    raw_term = orig_term;
    raw_term.c_lflag &= ~(ECHO | ICANON);
    raw_term.c_cc[VMIN] = 0;
    raw_term.c_cc[VTIME] = 0;
    tcsetattr(STDIN_FILENO, TCSANOW, &raw_term);
}

FBScreen::~FBScreen() {
    /* unset stdin */
    tcsetattr(STDIN_FILENO, TCSANOW, &orig_term);

    /* delete font */
    FT_Done_Face(face);
    FT_Done_FreeType(library);
    
    /* delete fb */
    delete [] draw_buffer;
    munmap(screen_buffer, screen_size);
    close(fbfd);
}

void FBScreen::init_font(std::string font_name, uint16_t size) {
    font_size = size;
    FT_Init_FreeType(&library);
    FT_New_Face(library, font_name.c_str(), 0, &face);
    FT_Set_Char_Size(face, size * size, 0, font_dpi, 0);
}

void FBScreen::draw_pixel(const Point point, const Color color) {
    if (point.x > (int32_t)vinfo.xres || point.x < 0 || point.y < 0 || point.y > (int32_t)vinfo.yres) {
        throw std::runtime_error("Point out of screen");
    }
    long int location =
        (point.x + vinfo.xoffset) * (vinfo.bits_per_pixel / 8) + (point.y + vinfo.yoffset) * finfo.line_length;
    if (vinfo.bits_per_pixel == 32) {
        *(draw_buffer + location + 0) = color.b;
        *(draw_buffer + location + 1) = color.g;
        *(draw_buffer + location + 2) = color.r;
        // no transparency
        *(draw_buffer + location + 3) = 0;
    } else {
        unsigned short int c = color.r << 11 | color.g << 5 | color.b;
        *((unsigned short int *)(draw_buffer + location)) = c;
    }
}

void FBScreen::draw_line_low(Point p1, Point p2, Color color) {
    auto dx = (int)p2.x - (int)p1.x;
    auto dy = (int)p2.y - (int)p1.y;
    auto yi = 0;
    if (dy < 0) {
        dy *= -1;
        yi = -1;
    } else {
        yi = 1;
    }
    auto d = (dy << 1) - dx;
    auto y = p1.y;
    for (auto x = p1.x; x < p2.x; x++) {
        draw_pixel({x, y}, color);
        if (d > 0) {
            y += yi;
            d -= dx << 1;
        }
        d += dy << 1;
    }
}

void FBScreen::draw_line_high(Point p1, Point p2, Color color) {
    auto dx = (int)p2.x - (int)p1.x;
    auto dy = (int)p2.y - (int)p1.y;
    auto xi = 0;
    if (dx < 0) {
        dx *= -1;
        xi = -1;
    } else {
        xi = 1;
    }
    auto d = (dx << 1) - dy;
    auto x = p1.x;
    for (auto y = p1.y; y < p2.y; y++) {
        draw_pixel({x, y}, color);
        if (d > 0) {
            x += xi;
            d -= dy << 1;
        }
        d += dx << 1;
    }
}

void FBScreen::draw_line(const Point p1, const Point p2, const Color color) {
    if (std::abs((int)p2.y - (int)p1.y) < std::abs((int)p2.x - (int)p1.x)) {
        if (p1.x > p2.x) {
            draw_line_low({p2.x, p2.y}, {p1.x, p1.y}, color);
        } else {
            draw_line_low({p1.x, p1.y}, {p2.x, p2.y}, color);
        }
    } else {
        if (p1.y > p2.y) {
            draw_line_high({p2.x, p2.y}, {p1.x, p1.y}, color);
        } else {
            draw_line_high({p1.x, p1.y}, {p2.x, p2.y}, color);
        }
    }
}

void FBScreen::draw_rect(const Point p1, const Point p2, const Color color) {
    Point z1 = {p1.x, p1.y};
    Point z2 = {p2.x, p1.y};
    Point z3 = {p2.x, p2.y};
    Point z4 = {p1.x, p2.y};

    draw_line(z1, z2, color);
    draw_line(z2, z3, color);
    draw_line(z3, z4, color);
    draw_line(z4, z1, color);
}

void FBScreen::draw_rect_fill(const Point p1, const Point p2, const Color color) {
    for (int32_t y = p1.y; y < p2.y; ++y) {
        draw_line({p1.x, y}, {p2.x, y}, color);
    }
}

void FBScreen::draw_text(const Point point, const Color color, const char *fmt, ...) {
    const int text_buffer_size = 1024;
    // prepare text
    char text[text_buffer_size] = {};
    va_list arg;
    va_start(arg, fmt);
    vsnprintf(text, text_buffer_size, fmt, arg);
    va_end(arg);

    Point pos = point;

    // render char glyph
    slot = face->glyph;
    for (uint32_t n = 0; n < strlen(text); n++) {
        if (text[n] == ' ') {
            pos.x += font_size / 2;
            continue;
        }
        // load
        if (FT_Load_Char(face, text[n], FT_LOAD_RENDER)) {
            // ignore errors
            continue;
        }
        // draw
        for (int32_t y = 0; y < (int32_t)slot->bitmap.rows; y++) {
            for (int32_t x = 0; x < (int32_t)slot->bitmap.width; x++) {
                uint8_t value = slot->bitmap.buffer[y * slot->bitmap.width + x];
                if (value == 0) {
                    continue;
                }
                float percent = value / 255.0;
                Color curr_c = {uint8_t(percent * color.r), uint8_t(percent * color.g), uint8_t(percent * color.b)};
                Point curr_p = {pos.x + x, pos.y + y - slot->bitmap_top + font_size / 2};
                draw_pixel(curr_p, curr_c);
            }
        }
        // move
        pos.x += slot->bitmap.width + (slot->bitmap.width / 3);
    }
}

void FBScreen::clear(const Color color) {
    draw_rect_fill({0, 0}, {(int32_t)vinfo.xres, (int32_t)vinfo.yres}, color);
}

void FBScreen::flush() {
    memcpy(screen_buffer, draw_buffer, screen_size);
}

int FBScreen::get_key() {
    char input_key;
    read(STDIN_FILENO, &input_key, 1);
    return input_key;
}

void FBView::update_state() {
    int key = screen->get_key();
    if (key == '\t') {
        next_focus();
        objects[prev_object]->focus_off();
        objects[curr_object]->focus_on();
    } else if (!objects.empty()) {
        objects[curr_object]->key_press(key);
    }
    screen->clear(clear_color);
    for (auto obj : objects) {
        obj->render(screen);
    }
    screen->flush();
}