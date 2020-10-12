#include <cstdio>
#include <vector>
#include <string>

std::vector<uint8_t> to_bcd(const std::string &data) {
    std::string input = data;
    if (data.size() % 2 != 0) {
        input += '0';
    }
    
    const size_t length = input.size() / 2;
    std::vector<uint8_t> result(length, 0);

    printf("length = %ld\n", length);

    for (size_t i = 0; i < input.size(); i += 2) {
        printf("i = %ld, i/2 = %ld\n", i, i / 2);
        result[i / 2] = (input[i + 0] - '0') << 4 | (input[i + 1] - '0');
    }

    return result;
}

void print(const std::vector<uint8_t> &input) {
    for (size_t i = 0; i < input.size(); i++) {
        printf("0x%02X ", input[i]);
    }
}

int main() {
    std::string demo = "911";
    std::vector<uint8_t> result = to_bcd(demo);
    print(result);
}