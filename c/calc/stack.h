#ifndef _STACK_H
#define _STACK_H

#include <stdlib.h>

void init_stack( size_t size );
void free_stack();

void push( double a );
double pop();

#endif
