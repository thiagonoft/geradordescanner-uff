%option noyywrap

%{
#include <stdio.h>

#define YY_DECL int yylex()

#include "parser.tab.h"

%}

/* 10 IF N = 0 THEN RETURN */
/* 10 LET N = 0 */

%%
[I][F]                   {return IF;}
[T][H][E][N]             {return THEN;}
[R][E][T][U][R][N]       {return RETURN;}
[L][E][T]                {return LET;}
[=]                      {return '=';}
[0-9]+                   {return Integer;}
[a-zA-Z]([0-9a-zA-Z])*   {return ID;}
\n	                     {return NewLine;}

%%