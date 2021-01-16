#pragma once
#include <iostream>
#include <stdarg.h>

void send_info(int count, ...);
void send_warning(const char *module, const char *info);
void send_error(const char *module, const char *info, int code);