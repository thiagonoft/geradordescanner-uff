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

%token Integer
%token String
%token Real
%token NewLine
%token ID
%token CLOSE DATA DIM END FOR GOTO GOSUB IF INPUT LET NEXT OPEN POKE PRINT READ RETURN RESTORE RUN STOP SYS WAIT Remark 
%token TO STEP AS THEN OUTPUT
%token OR AND NOT 
%token Branco

%token GREATER_OR_EQUAL_THAN ">="
%token LESS_OR_EQUAL_THAN "<="

%%

Lines: Integer Statements NewLine Lines 
                | Integer Statements NewLine {printf("%d\n", $1); }
;

Statements: Statement ':' Statements
                | Statement
;

Statement: CLOSE '#' Integer
                | DATA ConstantList 
                | DIM ID '(' IntegerList ')'
                | END          
                | FOR ID '=' Expression TO Expression     
                | FOR ID '=' Expression TO Expression STEP Integer
                | GOTO Expression 
                | GOSUB Expression 
                | IF Expression THEN Statement         
                | INPUT IDList       
                | INPUT '#' Integer ',' IDList       
                | LET ID '=' Expression 
                | NEXT IDList               
                | OPEN Value FOR Access AS '#' Integer
                | POKE ValueList
                | PRINT PrintList
                | PRINT '#' Integer ',' PrintList
                | READ IDList           
                | RETURN
                | RESTORE
                | RUN
                | STOP
                | SYS Value
                | WAIT ValueList
                | Remark
;

Access: INPUT
             | OUTPUT
;

IDList: ID ',' IDList 
             | ID 
;

ValueList: Value ',' ValueList 
                | Value 
;

ConstantList: Constant ',' ConstantList 
                | Constant 
;

IntegerList: Integer ',' IntegerList
                    | Integer
;

ExpressionList: Expression ',' ExpressionList 
                    | Expression 
;

PrintList: Expression ';' PrintList
                    | Expression 
                    | Branco
;

Expression: AndExp OR Expression 
                | AndExp 
;

AndExp: NotExp AND AndExp 
                | NotExp 
;

NotExp: NOT CompareExp 
                | CompareExp 
;

CompareExp: AddExp '='  CompareExp 
                // | AddExp '<>' CompareExp // que isso??
                // | AddExp '><' CompareExp // que isso??
                | AddExp '>'  CompareExp
                | AddExp GREATER_OR_EQUAL_THAN CompareExp
                | AddExp '<'  CompareExp
                | AddExp LESS_OR_EQUAL_THAN CompareExp
                | AddExp 
;

AddExp: MultExp '+' AddExp 
                | MultExp '-' AddExp 
                | MultExp 
;

MultExp: NegateExp '*' MultExp 
                | NegateExp '/' MultExp 
                | NegateExp 
;

NegateExp: '-' PowerExp 
                | PowerExp 
;

PowerExp: Value PowerExp2 
                | Value
;

PowerExp2: '^' PowerExp
;

Value: '(' Expression ')'
                | ID 
                | ID '(' ExpressionList ')'
                | Constant
;

Constant: Integer 
             | String 
             | Real 
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