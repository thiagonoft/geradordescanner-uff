%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(const char *s);
extern int yylex();
%}

%union {
    int ival;
    char *sval;
}

%token <sval> IDENTIFIER
%token <ival> NUMBER
%token PLUS MINUS MULTIPLY DIVIDE EQUALS
%token LPAREN RPAREN SEMICOLON
%token IF THEN ELSE FOR TO STEP WHILE PRINT INPUT DO

%left PLUS MINUS
%left MULTIPLY DIVIDE
%right EQUALS
%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%%
program:
    statement_list
    ;

statement_list:
    | statement_list statement
    ;

statement:
      assignment_statement SEMICOLON { printf("Processed an assignment.\n"); }
    | if_statement { printf("Processed an if statement.\n"); }
    | while_statement
    | for_statement
    | print_statement SEMICOLON { printf("Processed a print statement.\n"); }
    | input_message SEMICOLON
    ;

assignment_statement:
    IDENTIFIER EQUALS expression
    ;

expression:
      NUMBER
    | IDENTIFIER
    | expression PLUS expression
    | expression MINUS expression
    | expression MULTIPLY expression
    | expression DIVIDE expression
    | LPAREN expression RPAREN
    ;

if_statement:
    IF expression THEN statement_list %prec LOWER_THAN_ELSE
    | IF expression THEN statement_list ELSE statement_list
    ;

while_statement:
WHILE expression DO statement_list
;

for_statement:
FOR IDENTIFIER EQUALS expression TO expression STEP expression DO statement_list
;

print_statement:
PRINT expression
;

input_message:
INPUT IDENTIFIER
;

%%
void yyerror(const char *s) {
fprintf(stderr, "Error: %s\n", s);
}

int main() {
    yyparse();
    return 0;
}
