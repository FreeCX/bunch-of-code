#include <ctype.h>
#include <stdio.h>

int main( void )
{
    char A, Z;
    int c;

    while ( ( c = fgetc( stdin ) ) != EOF ) {
        if ( isupper( c ) ) {
            A = 'A'; Z = 'Z';
        } else {
            A = 'a'; Z = 'z';
        }
        if ( isalpha( c ) ) {
            fputc( Z - c + A, stdout );
        } else {
            fputc( c, stdout );
        }
    }
    return 0;
}
