// compile: gcc 2048_gl.c -O3 -lGL -lglut -lm -o 2048_gl
// based on https://github.com/mevdschee/2048.c
#include <GL/glut.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <time.h>
#include <math.h>

#define SIZE 4

typedef struct {
    GLubyte r;
    GLubyte g;
    GLubyte b;
} color;

int16_t board[SIZE][SIZE];
color c[] = {
    {140, 140, 140}, // 0
    {120, 150,  20}, // 2
    { 20, 130,  50}, // 4
    { 20, 130, 100}, // 8
    {200, 120,  30}, // 16
    {150, 100,  30}, // 32
    {150, 100, 150}, // 64
    {150,  50, 150}, // 128
    {150,  30, 100}, // 256
    {200,  30,  30}, // 512
    { 30,  50, 200}, // 1024
    {100, 100, 200}, // 2048
    {200,   0,  50}, // 4096
    {200, 200,  50}  // 8192
};

int w_width = 500;
int w_height = 500;
int win_id = 0;
GLfloat n = 60.0f;
GLfloat aspect;
int g_pause = 0;
int down = 0;

void spDrawString( float x, float y, const char *fmt, ... )
{
    char buffer[256];
    char * text = buffer;
    va_list ap;

    va_start( ap, fmt );
    vsprintf( text, fmt, ap );
    va_end( ap );
    glRasterPos2f( x, y );
    while ( *text ) {
        glutBitmapCharacter( GLUT_BITMAP_HELVETICA_18, *text++ );
    }
}

int8_t arrayLength( int16_t array[SIZE] ) 
{
    int8_t len = SIZE;

    while ( len > 0 && array[len-1] == 0 ) {
        len--;
    }
    return len;
}

int shiftArray( int16_t array[SIZE], int8_t start, int8_t length )
{
    int success = 0;
    int8_t x, i;

    for ( x = start; x < length - 1; x++ ) {
        while ( array[x] == 0 ) {
            for ( i = x; i < length - 1; i++ ) {
                array[i] = array[i+1];
                array[i+1] = 0;
                length = arrayLength( array );
                success = 1;
            }
        }
    }
    return success;
}

int collapseArray( int16_t array[SIZE], int8_t x ) 
{
    int success = 0;

    if ( array[x] == array[x+1] ) {
        if ( down == 1 ) {
            array[x] /= 2;
        } else {
            array[x] *= 2;
        }
        array[x+1] = 0;
        success = 1;
    }
    return success;
}

int condenseArray(int16_t array[SIZE]) 
{
    int success = 0;
    int8_t x, length;

    length = arrayLength( array );
    for ( x = 0; x < length - 1; x++ ) {
        length = arrayLength( array );
        success |= shiftArray( array, x, length );
        length = arrayLength( array );
        success |= collapseArray( array, x );
    }
    return success;
}

void rotateBoard( int16_t board[SIZE][SIZE] ) 
{
    int8_t i, j, n = SIZE;
    int16_t tmp;

    for ( i = 0; i < n / 2; i++ ) {
        for ( j = i; j < n - i - 1; j++ ) {
            tmp = board[i][j];
            board[i][j] = board[j][n-i-1];
            board[j][n-i-1] = board[n-i-1][n-j-1];
            board[n-i-1][n-j-1] = board[n-j-1][i];
            board[n-j-1][i] = tmp;
        }
    }
}

int moveUp( int16_t board[SIZE][SIZE] ) 
{
    int success = 0;
    int8_t x;

    for ( x = 0; x < SIZE; x++ ) {
        success |= condenseArray( board[x] );
    }
    return success;
}

int moveLeft( int16_t board[SIZE][SIZE] ) 
{
    int success;

    rotateBoard( board );
    success = moveUp( board );
    rotateBoard( board );
    rotateBoard( board );
    rotateBoard( board );
    return success;
}

int moveDown( int16_t board[SIZE][SIZE] ) 
{
    int success;

    rotateBoard( board );
    rotateBoard( board );
    success = moveUp( board );
    rotateBoard( board );
    rotateBoard( board );
    return success;
}

int moveRight( int16_t board[SIZE][SIZE] ) 
{
    int success;

    rotateBoard( board );
    rotateBoard( board );
    rotateBoard( board );
    success = moveUp( board );
    rotateBoard( board );
    return success;
}

int findPairDown( int16_t board[SIZE][SIZE] ) 
{
    int success = 0;
    int8_t x, y;

    for ( x = 0; x < SIZE; x++ ) {
        for ( y = 0; y < SIZE - 1; y++ ) {
            if ( board[x][y] == board[x][y+1] ) {
                return 1;
            }
        }
    }
    return success;
}

int16_t countEmpty( int16_t board[SIZE][SIZE] ) 
{
    int8_t x, y;
    int16_t count = 0;

    for ( x = 0; x < SIZE; x++ ) {
        for ( y = 0; y < SIZE; y++ ) {
            if ( board[x][y] == 0 ) {
                count++;
            }
        }
    }
    return count;
}

int gameEnded( int16_t board[SIZE][SIZE] )
{
    int ended = 1;

    if ( countEmpty( board ) > 0 ) {
        return 0;
    }
    if ( findPairDown( board ) ) {
        return 0;
    }
    rotateBoard( board );
    if ( findPairDown( board ) ) {
        ended = 0;
    }
    rotateBoard( board );
    rotateBoard( board );
    rotateBoard( board );
    return ended;
}

void addRandom( int16_t board[SIZE][SIZE] ) 
{
    static int initialized = 0;
    int8_t x, y;
    int16_t r, len = 0;
    int16_t n, list[SIZE*SIZE][2];

    if ( !initialized ) {
        srand( time( NULL ) );
        initialized = 1;
    }
    for ( x = 0; x < SIZE; x++ ) {
        for ( y = 0; y < SIZE; y++ ) {
            if ( board[x][y] == 0 ) {
                list[len][0] = x;
                list[len][1] = y;
                len++;
            }
            if ( board[x][y] == 2048 ) {
                down = 1;
            }
        }
    }
    if ( len > 0) {
        r = rand()%len;
        x = list[r][0];
        y = list[r][1];
        n = (rand()%2+1)*2;
        if ( down == 1 ) {
            n = -n;
        }
        board[x][y] = n;
    }
}

void new_game( void )
{
    memset( board, 0, sizeof(board) );
    addRandom( board );
    addRandom( board );
}

void program_init( void )
{
    GLint sw = glutGet( GLUT_SCREEN_WIDTH );
    GLint sh = glutGet( GLUT_SCREEN_HEIGHT );
    glutPositionWindow( ( sw - w_width ) / 2, ( sh - w_height) / 2 );
    glClearColor( 0.0f, 0.0f, 0.0f, 1.0f );
    new_game();
}

void program_render( void )
{
    int i, j, value;
    const float k = n / SIZE;

    glClear( GL_COLOR_BUFFER_BIT );
    glPointSize( 50.0f );
    glBegin( GL_POINTS );
    for ( i = 0; i < SIZE; i++ ) {
        for ( j = 0; j < SIZE; j++ ) {
            value = (int)( log2( board[i][j]+1 ) );
            glColor3ub( c[value].r, c[value].g, c[value].b );
            glVertex2f( (i-1.5)*k, (SIZE-j-2.5)*k );
        }
    }
    glEnd();
    glColor3f( 1.0f, 1.0f, 1.0f );
    for ( i = 0; i < SIZE; i++ ) {
        for ( j = 0; j < SIZE; j++ ) {
            if ( board[i][j] != 0 ) {
                value = (int)log10( board[i][j] ) + 1;
                spDrawString( (i-0.08*value-1.5)*k, (SIZE-j-2.6)*k, 
                    "%d", board[i][j] );
            }
        }
    }
    glutSwapBuffers();
}

void program_redraw( int value )
{
    static int move = 0, success;
    if ( g_pause == 1 ) {
        move++;
        switch ( move ) {
            case 1:
                success = moveLeft( board );
                break;
            case 2:
                success = moveRight( board );
                break;
            case 3:
                success = moveUp( board );
                break;
            case 4:
                success = moveDown( board );
                move = 0;
                break;
        }
        if ( success ) {
            addRandom( board );
            if ( gameEnded( board ) ) {
                new_game();
            }
        }
    }
    program_render();
    glutTimerFunc( 100, program_redraw, 0 );
}

void program_resize( int width, int height )
{
    aspect = (float) width / height;
    glViewport( 0, 0, width, height );
    glMatrixMode( GL_PROJECTION );
    glLoadIdentity();
    if ( width <= height ) {
        glOrtho( -n, n, -n/aspect, n/aspect, n, -n );
    } else {
        glOrtho( -n * aspect, n * aspect, -n, n, n, -n );
    }
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}
void program_keyboard( unsigned char key, int x, int y )
{
    int success;

    switch ( key ) {
        case 'q':
            glutDestroyWindow( win_id );
            break;
        case 'a':
            success = moveLeft( board );
            break;
        case 'd':
            success = moveRight( board );
            break;
        case 'w':
            success = moveUp( board );
            break;
        case 's':
            success = moveDown( board );
            break;
        case ' ':
            g_pause = !g_pause;
            break;
        default:
            success = 0;
            break;
    }
    if ( success ) {
        addRandom( board );
        if ( gameEnded( board ) ) {
            new_game();
        }
    }
}

void program_free( void )
{
}

int main( int argc, char *argv[] )
{
    glutInit( &argc, argv );
    glutInitWindowSize( w_width, w_height );
    glutInitWindowPosition( 0, 0 );
    glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE );
    win_id = glutCreateWindow( "2048" );
    glutReshapeFunc( program_resize );
    glutDisplayFunc( program_render );
    glutKeyboardFunc( program_keyboard );
    glutTimerFunc( 1, program_redraw, 0 );
    program_init();
    glutMainLoop();
    program_free();
    return EXIT_SUCCESS;
}
