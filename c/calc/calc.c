#include "calc.h"
#include "stack.h"

int main()
{
	int digit = 0;
	char dig[64];
	double number = 0;
	double op = 0;
	int n = 0;
	int c;

	init_stack( 100 );
    while ( ( c = getchar() ) != ESC ) {
    	switch ( getinfo( c ) ) {
    		case IS_NUMBER:
    			dig[n++] = c;
    			digit = 1;
    			break;
    		case IS_NEXT:
    			if ( digit ) {
    				dig[n] = '\0';
                    number = strtod( dig, NULL );
    				push( number );
    				n = 0;
    				number = 0;
    			}
    			break;
    		case IS_END:
    			printf( "= %f\n", pop() );
    			break;
    		case '+':
    			push( pop() + pop() );
    			digit = 0;
    			break;
    		case '-':
    			op = pop();
    			push( pop() - op );
    			digit = 0;
    			break;
    		case '*':
    			push( pop() * pop() );
    			digit = 0;
    			break;
    		case '/':
    			op = pop();
    			if ( op != 0.0 ) {
    				push(pop() / op);
                } else {
    				printf("divide by zero!\n");
                }
    			digit = 0;
    			break;
    		case '^':
    			op = pop();
    			push( pow( pop(), op ) );
    			break;
            default:
                break;
    	}
    }
    free_stack();
    return 0;
}
