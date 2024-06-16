%option noyywrap

%{
#include <stdio.h>

#define YY_DECL int yylex()

#include "parser.tab.h"

%}

%%
"quit" {return T_QUIT;}

[0-9]+ {return T_NUMBER;}
[a-zA-Z]([0-9a-zA-Z])* {return T_IDENTIFIER;}
\n	        {return T_NEWLINE;}
%%