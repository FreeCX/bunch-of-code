#include "error.hpp"

void send_message(const char * type, const char * module, const char * info) {
    std::cerr << "[" << type << "::" << module << "]:" << info << std::endl;
}

void send_info(int count, ...) {
    va_list arguments;
    va_start(arguments, count);
    std::cout << "[info]: ";
    for (int i = 0; i < count; i++) {
        const char * arg = va_arg(arguments, const char *);
        std::cout << arg;
    }
    va_end(arguments);
    std::cout << std::endl; 
}

void send_warning(const char * module, const char * info) {
    send_message("warning", module, info);
}

void send_error(const char * module, const char * info, int code) {
    send_message("error", module, info);
    exit(code);
}