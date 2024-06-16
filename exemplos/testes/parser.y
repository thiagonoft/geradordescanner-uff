%{

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex();
extern int yyparse();
extern FILE* yyin;
extern char* yytext;

void yyerror(const char* s);
%}

%union {
	char* TYPE_STRING;
	int TYPE_INTEGER;
}

%token<TYPE_STRING> T_IDENTIFIER
%token<TYPE_INTEGER> T_NUMBER
%token T_NEWLINE T_QUIT

%type<TYPE_STRING> id

%start computation

%%

computation:
		| computation line
;

line: T_NEWLINE
    | id T_NEWLINE { printf("\tResult: %s\n", $1); }
    | T_QUIT T_NEWLINE { printf("bye!\n"); exit(0); }

id: T_IDENTIFIER { $$ = strdup(yytext); }
;

/* id: T_IDENTIFIER
    | T_IDENTIFIER T_NEWLINE // { printf("\tResult: %s\n", $$); }
; */

/* expression: T_IDENTIFIER { $$ = $1; }
; */

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