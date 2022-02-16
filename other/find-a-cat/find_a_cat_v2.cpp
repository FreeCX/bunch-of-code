#include <iostream>
#include <limits>
#include <string>

#include "xorshift.hpp"

const uint32_t ascii_max = 255;
const char c_symb = 'c';

bool is_cat(uint32_t c, uint32_t a, uint32_t t) {
    return char(c % ascii_max) == c_symb and char(a % ascii_max) == 'a' and char(t % ascii_max) == 't';
}

uint32_t n_vals(uint32_t i) {
    return ascii_max * i + uint8_t(c_symb);
}

uint32_t xorshift_backward(uint32_t seed) {
    uint32_t f0 = (seed ^ (seed << 5)) & 0xFF;
    uint32_t f1 = (seed ^ (f0 << 5)) & 0xFFF;
    f0 = (seed ^ (f1 << 5)) & 0xFFFF;
    f1 = (seed ^ (f0 << 5)) & 0xFFFFF;
    f0 = (seed ^ (f1 << 5)) & 0xFFFFFF;
    f1 = (seed ^ (f0 << 5)) & 0xFFFFFFF;
    seed ^= f1 << 5;
    seed ^= seed >> 17;
    return seed ^ (((seed ^ (seed << 13)) & 0x00FFFFFF) << 13);
}

int main() {
    for (uint32_t i = 0; i < std::numeric_limits<uint32_t>::max(); i++) {
        uint32_t c = n_vals(i);
        uint32_t a = xorshift(c);
        uint32_t t = xorshift(a);
        if (is_cat(c, a, t)) {
            uint32_t seed = xorshift_backward(c);
            std::cout << "found " << seed << " at step " << i << std::endl;
            return 0;
        }
    }
}
