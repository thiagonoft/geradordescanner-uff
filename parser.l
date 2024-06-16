%option noyywrap

%{
#include <stdio.h>

#define YY_DECL int yylex()

#include "parser.tab.h"

%}
/*([0-9a-zA-Z])*/
%%
[a-zA-Z] {return T_IDENTIFIER;}

%%