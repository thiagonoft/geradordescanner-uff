%{
#include "basic.tab.h"
%}

%%

"IF"               { printf("Token: IF\n"); return IF; }
"THEN"             { printf("Token: THEN\n"); return THEN; }
"ELSE"             { printf("Token: ELSE\n"); return ELSE; }
"FOR"              { printf("Token: FOR\n"); return FOR; }
"TO"               { printf("Token: TO\n"); return TO; }
"STEP"             { printf("Token: STEP\n"); return STEP; }
"WHILE"            { printf("Token: WHILE\n"); return WHILE; }
"PRINT"            { printf("Token: PRINT\n"); return PRINT; }
"INPUT"            { printf("Token: INPUT\n"); return INPUT; }
[0-9]+             { printf("Token: NUMBER (%s)\n", yytext); yylval.ival = atoi(yytext); return NUMBER; }
[a-zA-Z][a-zA-Z0-9]* { printf("Token: IDENTIFIER (%s)\n", yytext); yylval.sval = strdup(yytext); return IDENTIFIER; }
"+"                { printf("Token: PLUS\n"); return PLUS; }
"-"                { printf("Token: MINUS\n"); return MINUS; }
"*"                { printf("Token: MULTIPLY\n"); return MULTIPLY; }
"/"                { printf("Token: DIVIDE\n"); return DIVIDE; }
"="                { printf("Token: EQUALS\n"); return EQUALS; }
"("                { printf("Token: LPAREN\n"); return LPAREN; }
")"                { printf("Token: RPAREN\n"); return RPAREN; }
";"                { printf("Token: SEMICOLON\n"); return SEMICOLON; }
[\t\r\n]+          { /* ignore whitespace */ }
" "                { /* ignore spaces */ }
.                  { printf("Token: OTHER (%c)\n", *yytext); return *yytext; }

%%

int yywrap() { return 1; }
