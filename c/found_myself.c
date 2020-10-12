#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void find_me( char **path )
{
    size_t min_size = 256;
    *path = (char *) calloc( min_size, sizeof(char) );
    readlink( "/proc/self/exe", *path, min_size * sizeof(char));
}

int main( int argc, char *argv[] )
{
    char *path;
    find_me( &path );
    printf( "[+] Found myself: '%s'\n", path );
    return 0;
}
