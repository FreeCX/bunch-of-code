#pragma once
#include <cstdarg>
#include <iostream>

void send_info(int count, ...);
void send_warning(const char *module, const char *info);
void send_error(const char *module, const char *info, int code);
