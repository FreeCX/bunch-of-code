#ifndef _CALC_H
#define _CALC_H

#include <stdio.h>
#include <math.h>

#define ESC	27

enum {
	IS_NUMBER,
	IS_NEXT,
	IS_END
};

int getinfo( int a )
{
	if ( ( a >= '0' && a <= '9' ) || (a == '.' || a == ',') ) {
		return IS_NUMBER;
    } else if ( a == ' ' ) {
		return IS_NEXT;
    } else if ( a == '\n' ) {
		return IS_END;
    } else {
		return a;
    }
}

#endif