%option noyywrap

%{
#include <stdio.h>

#define YY_DECL int yylex()

#include "calc.tab.h"
#include <math.h>


int convertFromOctToDec(const char* s) {
    int decimal = 0;

    int numLen = 0;
    while(s[numLen] != 'o')
    {
        numLen++;
    }

    // printf("numLen = %d\n", numLen);

    for(int i = 0; i < numLen;i++)
    {
        // printf("s[i] = %c\n", s[i]);
        // printf("(numLen - i - 1) = %d\n", (numLen - i - 1));
        // printf("(s[i] - '0') = %d\n", (s[i] - '0'));
        
        int digit = (int)(s[i] - '0');
        int exp = (numLen - i - 1);
        decimal += digit * pow(8, exp);

        // printf("decimal = %d\n", decimal);
    }

	return decimal;
}

%}

%%

[ \t]	; // ignore all whitespace
[0-9]+      {yylval.ival = atoi(yytext); return T_INT;} /* decimal */
[0-7]+[o]   {yylval.ival = convertFromOctToDec(yytext); return T_OCT;} /* octal */
\n	        {return T_NEWLINE;}
"+"		    {return T_PLUS;}
"-"		    {return T_MINUS;}
"*"		    {return T_MULTIPLY;}
"/"		    {return T_DIVIDE;}
"("		    {return T_LEFT;}
")"		    {return T_RIGHT;}
"exit"		{return T_QUIT;}
"quit"		{return T_QUIT;}

%%
