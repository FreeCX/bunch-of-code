#include <iostream>

#include "xorshift.hpp"

int main(int argc, char **argv) {
    if (argc < 3) {
        std::cout << "usage: " << argv[0] << " seed count" << std::endl;
        return 0;
    }

    uint32_t seed = atoi(argv[1]);
    uint32_t count = atoi(argv[2]);

    std::cout << "result: ";
    while (count--) {
        seed = xorshift(seed);
        std::cout << char(seed % 255);
    }
    std::cout << std::endl;
}
