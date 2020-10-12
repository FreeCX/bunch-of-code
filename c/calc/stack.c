#include <stdio.h>
#include <string.h>
#include "stack.h"

static double *stack;
static double *stack_new;
static size_t count = 0;
static size_t stack_size;

void init_stack( size_t size )
{
	stack_size = size * sizeof( double );
    stack = (double *) malloc( stack_size );
}

void free_stack()
{
    free( stack );
}

void push( double a )
{
	if ( ( count - 1 ) * sizeof( double ) > stack_size ) {
		stack_size *= 2;
        stack_new = (double *) realloc( stack, stack_size );
		stack = stack_new;
	}
    stack[count++] = a;
}

double pop()
{
	if (count != 0) {
		return stack[--count];
    } else {
		puts( "stack is empty!" );
		return 0.0;
	}
}

void print_stack()
{
    size_t i = count - 1;

    puts( "----------" );
    do {
        printf( "%lu: %lf\n", i, stack[i] );
    } while ( i > 0 );
   	puts( "----------" );
}
