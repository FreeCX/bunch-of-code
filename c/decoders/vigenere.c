#include <ctype.h>
#include <stdio.h>
#include <string.h>

#define ABC 26

int main( int argc, char *argv[] )
{
    size_t i = 0, code_size;
    int c;

    if ( argc > 1 ) {
        code_size = strlen( argv[1] );
        while ( ( c = fgetc( stdin ) ) != EOF ) {
            if ( i == code_size ) {
                i = 0;
            }
            if ( isalpha( c ) ) {
                fputc( ( c - argv[1][i] + ABC ) % ABC + ( isupper( c ) ? 'A' : 'a' ), stdout );
                i++;
            } else {
                fputc( c, stdout );
            }
        }
    }
    return 0;
}
