#include <iostream>
#include <string>

#include "xorshift.hpp"

bool is_cat(const std::string & word) {
    if (word.size() == 3) {
        return word[0] == 'c' and word[1] == 'a' and word[2] == 't';
    }
    return false;
}

int main() {
    std::string word = "";
    uint32_t seed = 42;
    uint32_t last_seed = seed;
    uint64_t steps = 0;

    while (true) {
        seed = xorshift(seed);
        steps += 1;
        uint8_t v = seed % 255;
        if (isalpha(v)) {
            word.push_back(char(v));
        } else {
            if (is_cat(word)) {
                std::cout << "found [" << last_seed << "] with " << steps << " steps: " << word << std::endl;
                return 0;
            }
            last_seed = seed;
            word = "";
        }
    }
}
