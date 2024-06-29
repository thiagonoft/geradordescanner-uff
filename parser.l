%{
#include "parser.tab.h"
%}

%%

"REM"[ \t]+[^\n]*          { return Remark; }
"IF"                  { return IF; }
"THEN"                { return THEN; }
"FOR"                 { return FOR; }
"TO"                  { return TO; }
"STEP"                { return STEP; }
"PRINT"               { return PRINT; }
"INPUT"               { return INPUT; }
"NEXT"                { return NEXT; }
"GOTO"                { return GOTO; }
"GOSUB"               { return GOSUB; }
"RETURN"              { return RETURN; }
"END"                 { return END; }
"DIM"                 { return DIM; }
"READ"                { return READ; }
"DATA"                { return DATA; }
"RESTORE"             { return RESTORE; }
"POKE"                { return POKE; }
"STOP"                { return STOP; }
"RUN"                 { return RUN; }
"SYS"                 { return SYS; }
"WAIT"                { return WAIT; }
"OPEN"                { return OPEN; }
"OUTPUT"              { return OUTPUT; }
"NOT"                 { return NOT; }
"AND"                 { return AND; }
"OR"                  { return OR; }
"CLOSE"               { return CLOSE; }
"LET"                 { return LET; }
"AS"                  { return AS; }

"<>"                  { return NOT_EQUAL_TO_A; }
"><"                  { return NOT_EQUAL_TO_B; }
">="                  { return GREATER_OR_EQUAL_THAN; }
"<="                  { return LESS_OR_EQUAL_THAN; }
">"                   { return '>'; }
"<"                   { return '<'; }
"="                   { return '='; }
"+"                   { return '+'; }
"-"                   { return '-'; }
"*"                   { return '*'; }
"/"                   { return '/'; }
"^"                   { return '^'; }

";"                   { return ';'; }
"("                   { return '('; }
")"                   { return ')'; }

[0-9]+                { yylval.ival = atoi(yytext); return Integer; }
[a-zA-Z][a-zA-Z0-9]*[$%]?  { yylval.sval = strdup(yytext); return ID; }
\"[^"]*\"         { yylval.sval = strdup(yytext); return String; }
[\t\r]+             { /* Ignorar espaços em branco */ }
" "                   { /* Ignorar espaços simples */ }
\n                    { return NewLine; }
.                     { return *yytext; }

%%

// [0-9]+\.[0-9]+         { yylval.real = atof(yytext); return Real; }
int yywrap() { return 1; }