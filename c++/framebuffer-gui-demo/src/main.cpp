#include "fb_gui.hpp"

class Label : public Object {
public:
    Point pos;
    std::string text;

    Label(const Point p, std::string t) : pos(p), text(t) {}
};

class Edit : public Object {
public:
    Point pos;
    Point size;
    std::string text;

    Edit(const Point p1, const Point p2) : pos(p1), size(p2), text("") {}
};

void edit_render(Screen * screen, Object * object) {
    Edit * e = (Edit *) object;
    screen->draw_rect_fill(e->pos, e->size, {40, 50, 50});
    if (e->is_focused()) {
        screen->draw_rect(e->pos, e->size, {255, 255, 255});
    }
    Point corr_pos = {e->pos.x + 5, e->pos.y + 5};
    screen->draw_text(corr_pos, {255, 255, 255}, e->text.c_str());
}

void edit_key_press(int key, Object * object) {
    Edit * e = (Edit *) object;
    if (key == 0x7F) {
        if (!e->text.empty()) {
            e->text.pop_back();
        }
    } else if (key >= 0x20 && key <= 0x7E) {
        e->text.push_back(key);
    }
}

void label_render(Screen * screen, Object * object) {
    Label * l = (Label *) object;
    screen->draw_text(l->pos, {255, 127, 0}, l->text.c_str());
}

int main() {
    FBScreen screen("/dev/fb0");
    screen.init_font("./resource/FiraMono-Regular.ttf", 32);

    FBView view(&screen);
    view.set_bg_color({0, 0, 0});
    
    Label label_a({10, 20}, "Enter A:");
    label_a.on_render(label_render);
    view.push_object(&label_a);

    Edit edit_a({10, 50}, {200, 80});
    edit_a.on_render(edit_render);
    edit_a.on_key_press(edit_key_press);
    view.push_object(&edit_a);

    Label label_b({10, 90}, "Enter B:");
    label_b.on_render(label_render);
    view.push_object(&label_b);

    Edit edit_b({10, 120}, {200, 150});
    edit_b.on_render(edit_render);
    edit_b.on_key_press(edit_key_press);
    view.push_object(&edit_b);

    while (screen.loop()) {
        view.update_state();
        usleep(50 * 1000);
    }
}