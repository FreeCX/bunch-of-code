#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

#define ABC 26

int main( int argc, char *argv[] )
{
    int k, c;

    if ( argc > 1 ) {
        k = atoi( argv[1] );
        while ( ( c = fgetc( stdin ) ) != EOF ) {
            if ( isalpha( c ) ) {
                fputc( ( c - 'A' - k + ABC ) % ABC + ( isupper( c ) ? 'A' : 'a' ), stdout );
            } else {
                fputc( c, stdout );
            }
        }
    }
    return 0;
}
