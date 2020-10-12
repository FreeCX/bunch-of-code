#include <stdio.h>

int main( void )
{
    int n = 7, key = 0, c;

    while ( 1 ) {
        c = fgetc( stdin );
        switch ( c ) {
            case '0':
            case '1':
                if ( n == 0 ) {
                    n = 7;
                    key += c - '0';
                    fputc( key, stdout );
                    key = 0;
                    continue;
                }
                key += ( c - '0' ) << n;
                n--;
                break;
            case '\n':
            case EOF:
                return 0;
            default:
                fputc( c, stdout );
        }
    }
    return 0;
}
