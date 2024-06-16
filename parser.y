%{

#include <stdio.h>
#include <stdlib.h>

extern int yylex();
extern int yyparse();
extern FILE* yyin;

void yyerror(const char* s);
%}

%token T_IDENTIFIER
%token T_NEWLINE

%start new_line

%%

computation:
	   | computation line
;

line: T_NEWLINE
    | expression T_NEWLINE { printf("\tResult: %s\n", $1); }
;

expression: T_IDENTIFIER				{ $$ = $1; }
;

%%

int main() {
	yyin = stdin;

	do {
		yyparse();
	} while(!feof(yyin));

	return 0;
}

void yyerror(const char* s) {
	fprintf(stderr, "Parse error: %s\n", s);
	exit(1);
}