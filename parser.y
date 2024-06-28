%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Symbol {
    char *name;
    char *type; // "int", "float", etc.
    struct Symbol *next; // Para colisões em um possível hashing
} Symbol;

#define HASH_SIZE 101
static Symbol *symbol_table[HASH_SIZE];

unsigned hash(char *str) {
    unsigned hashval;
    for (hashval = 0; *str != '\0'; str++)
        hashval = *str + 31 * hashval;
    return hashval % HASH_SIZE;
}

Symbol *lookup_symbol(char *name) {
    Symbol *sp;
    for (sp = symbol_table[hash(name)]; sp != NULL; sp = sp->next) {
        if (strcmp(name, sp->name) == 0)
            return sp;
    }
    return NULL;
}

Symbol *insert_symbol(char *name, char *type) {
    unsigned hashval;
    Symbol *sp = lookup_symbol(name);
    if (sp == NULL) {
        sp = (Symbol *)malloc(sizeof(*sp));
        if (sp == NULL || (sp->name = strdup(name)) == NULL)
            return NULL;
        sp->type = strdup(type);
        hashval = hash(name);
        sp->next = symbol_table[hashval];
        symbol_table[hashval] = sp;
    } else {
        free(sp->type);
        sp->type = strdup(type);
    }
    return sp;
}

extern int yylex();
extern int yyparse();
extern FILE* yyin;
extern char* yytext;

void yyerror(const char* s);
%}


%union {
    int ival; // For integers
    char* sval; // For strings like identifiers
}


%token <ival> Integer
%token String
%token Real
%token NewLine
%token <sval> ID
%token CLOSE DATA DIM END FOR GOTO GOSUB IF INPUT LET NEXT OPEN POKE PRINT READ RETURN RESTORE RUN STOP SYS WAIT Remark 
%token TO STEP AS THEN OUTPUT
%token OR AND NOT 
%token Branco

%token GREATER_OR_EQUAL_THAN ">="
%token LESS_OR_EQUAL_THAN "<="

%%

Lines: Integer Statements NewLine Lines 
                | Integer Statements NewLine
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
                /* | LET ID '=' Expression */
                | LET ID '=' Expression {
                    Symbol *sym = lookup_symbol($2);  // Aqui $2 deve ser do tipo char*
                    if (sym == NULL) {
                        // Declaração implícita se não encontrada na tabela
                        sym = insert_symbol($2, "generic"); // Considera-se tipo genérico
                        if (sym == NULL) {
                            yyerror("Memory error: could not declare variable");
                        }
                    }
                    // Aqui você pode adicionar código para lidar com a atribuição
                    printf("Variable %s set.\n", $2);
                }
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