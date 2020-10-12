// gcc matrix.c `ncursesw6-config --cflags --libs` -o matrix
#include <locale.h>
#include <ncurses.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <wchar.h>

#define COUNT 100
#define SLEEP 30000

typedef struct {
    wchar_t buf;
    int x, y, yl;
} line;

wchar_t symb[] = 
    L"abcdefghijklmnopqrstuvwxyz"
    L"абвгдеёжзийклмнопрстуфхцчшщьъыжэюя"
    L"1234567890";
line p[COUNT];

void draw( void )
{
    int rnd, l, i;
    wchar_t chr;

    l = wcslen( symb );
    while ( 1 ) {
        for ( i = 0; i < COUNT; i++ ) {
            rnd = rand()%l;
            if ( p[i].y == LINES - 1 ) {
                p[i].x = 2 * ( rand()% ( COLS / 2 ) );
                p[i].y = rand() % LINES;
            } else {
                p[i].y++;
            }
            chr = *(symb+rnd);
            move( p[i].yl, p[i].x );
            attron( A_BOLD | COLOR_PAIR(1) );
            if ( i % 2 == 0 ) {
                addch( ' ' );
            } else {

                printw( "%lc", p[i].buf );
            }
            move( p[i].y, p[i].x );
            attron( A_BOLD | COLOR_PAIR(2) );
            if ( i % 2 == 0 ) {
                addch( ' ' );
            } else {
                printw( "%lc ", chr );
            }
            move( 0, 0 );
            refresh();
            p[i].yl = p[i].y;
            p[i].buf = chr;
        }
        usleep( SLEEP );
    }
}

int main( int argc, char *argv[] )
{
    int i;
    
    setlocale( LC_ALL, "" );
    srand( time( NULL ) );
    initscr();
    cbreak();
    noecho();
    start_color();
    for ( i = 0; i < COUNT; i++ ) {
        p[i].x = rand() % COLS;
        p[i].y = rand() % LINES;
        p[i].yl = rand() % LINES;
    }
    init_pair( 1, COLOR_GREEN, COLOR_BLACK );
    init_pair( 2, COLOR_WHITE, COLOR_BLACK );
    draw();
    attroff( A_BOLD | COLOR_PAIR(1) );
    attroff( A_BOLD | COLOR_PAIR(2) );
    endwin();
    return 0;
}
