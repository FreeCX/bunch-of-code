#include <stdio.h>
#include <ctype.h>
#include <math.h>

int main( void )
{
    int c, a;

    c = a = 0;
    while ( 1 ) {
        c = fgetc( stdin );
        if ( isdigit( c ) ) {
            a = a * 10 + ( c - '0' );
            continue;
        }
        a += 'a' - 1;
        if ( isalpha( a ) ) {
            fputc( a, stdout );
        }
        if ( c == EOF ) {
            break;
        }
        a = 0;
        fputc( c, stdout );
    }
    return 0;
}