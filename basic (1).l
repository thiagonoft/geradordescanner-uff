%{
#include "basic.tab.h"
%}

%%

"REM"[ \t]+[^\n]*          { return REMARK; }
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

">="                  { return GREATER_OR_EQUAL_THAN; }
"<="                  { return LESS_OR_EQUAL_THAN; }
">"                   { return '>'; }
"<"                   { return '<'; }
"="                   { return EQUALS; }
"+"                   { return PLUS; }
"-"                   { return MINUS; }
"*"                   { return MULTIPLY; }
"/"                   { return DIVIDE; }
"^"                   { return '^'; }

";"                   { return SEMICOLON; }
"("                   { return LPAREN; }
")"                   { return RPAREN; }

[0-9]+                { yylval.ival = atoi(yytext); return INTEGER; }
[a-zA-Z][a-zA-Z0-9]*[$%]?  { yylval.sval = strdup(yytext); return ID; }
\"[^"]*\"         { yylval.sval = strdup(yytext); return STRING; }
[0-9]+\.[0-9]+         { yylval.real = atof(yytext); return REAL; }

[\t\r\n]+             { /* Ignorar espaços em branco */ }
" "                   { /* Ignorar espaços simples */ }
.                     { return *yytext; }

%%

int yywrap() { return 1; }