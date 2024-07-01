%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Symbol {
    char* name;
    char* type; // "int", "float", "string"
    struct Symbol* next; // For collision handling in hash table
} Symbol;

#define HASH_SIZE 101
static Symbol* symbol_table[HASH_SIZE];

// Hash function
unsigned hash(char* str){
    unsigned hashval;
    for(hashval = 0; *str != '\0'; str++){
        hashval = *str + 31 * hashval;
    }
    return hashval % HASH_SIZE;
}

Symbol* lookup_symbol(char *name){
    Symbol* sp;
    for(sp = symbol_table[hash(name)]; sp != NULL; sp = sp->next){
        if(strcmp(name, sp->name) == 0)
            return sp;
    }
    return NULL;
}

Symbol* insert_symbol(char *name, char *type){
    unsigned hashval;
    Symbol* sp = lookup_symbol(name);
    if(sp == NULL){
        sp = (Symbol*) malloc(sizeof(*sp));
        if(sp == NULL || (sp->name = strdup(name)) == NULL)
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

// GRAMMAR
char* get_variable_type(char* ID){
    Symbol* sym = lookup_symbol(ID);
    if(sym == NULL){
        yyerror("Undeclared variable");
        return NULL;
    }
    return sym->type;
}

void handle_arithmetic_types(char* typeA, char* typeB){
    if((
        (
            (strcmp(typeA, "int") != 0)
         && (strcmp(typeA, "float") != 0)
        )
    )
        || 
    (
        (
            (strcmp(typeB, "int") != 0)
         && (strcmp(typeB, "float") != 0)
        )
    ))
    {
        yyerror("Type error - Arithmetic operation with non-numeric type");
    }
}

void handle_equal_types(char* typeA, char* typeB){
    if(strcmp(typeA, typeB) != 0){
        yyerror("Type error - Operation between two different types");
    }
}

void handle_non_numeric(char* type)
{
    if(strcmp(type, "string") == 0){
        yyerror("Type error - Expected numeric type");
    }
}

void declare_variable_on_let(char* ID, char* type){
    Symbol* sym = lookup_symbol(ID);
    if(sym == NULL){
        sym = insert_symbol(ID, type);
        if(sym == NULL){
            yyerror("Memory error: could not declare variable");
        } else {
            printf("Variable %s explicitly set to type %s\n", ID, type);
        }
    } else {
        if(strcmp(sym->type, type) != 0){
            yyerror("Type error - Variable redeclared with a different type");
        }
    }
}

void declare_variable_on_for(char* ID){
    Symbol* sym = lookup_symbol(ID);
    if(sym == NULL){
        sym = insert_symbol(ID, "int");
        if(sym == NULL){
            yyerror("Memory error: could not declare variable");
        } else {
            printf("Variable %s implicitly set to type int\n", ID);
        }
    } else {
        handle_equal_types(sym->type, "int");
    }
}

bool check_if_variable_is_declared(char* ID){
    Symbol* sym = lookup_symbol(ID);
    if(sym == NULL){
        return false;
    }
    return true;
}

%}

%union {
    int ival;
    char* sval;
    float fval;
    char* type;
}

%token <ival> Integer
%token <sval> String
%token <fval> Real
%token NewLine
%token <sval> ID
%token CLOSE DATA DIM END FOR GOTO GOSUB IF INPUT LET NEXT OPEN POKE PRINT READ RETURN RESTORE RUN STOP SYS WAIT Remark
%token TO STEP AS THEN OUTPUT
%token OR AND NOT
%token Branco

%token NOT_EQUAL_TO_A "<>"
%token NOT_EQUAL_TO_B "><"
%token GREATER_OR_EQUAL_THAN ">="
%token LESS_OR_EQUAL_THAN "<="

%type <type> Constant Expression AndExp NotExp CompareExp AddExp MultExp NegateExp PowerExp PowerExp2 Value

%%

Lines: Integer Statements NewLine Lines
                | Integer Statements NewLine
;

Statements: Statement ':' Statements
                | Statement
;

Statement: CLOSE '#' Integer
                | DATA ConstantList
                | DIM ID '(' IntegerList ')' {
                    declare_variable_on_let($2, "int");
                }
                | END
                | FOR ID '=' Expression TO Expression {
                    declare_variable_on_for($2);
                }
                | FOR ID '=' Expression TO Expression STEP Integer {
                    declare_variable_on_for($2);
                }
                | GOTO Expression
                | GOSUB Expression
                | IF Expression THEN Statement
                | INPUT IDList
                | INPUT '#' Integer ',' IDList
                | LET ID '=' Expression {
                    declare_variable_on_let($2, $4);
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

Expression: AndExp OR Expression {
                    handle_equal_types($1, $3);
                    $$ = $1; // Assume OR expressions yield the same type
                }
                | AndExp {
                    $$ = $1;
                }
;

AndExp: NotExp AND AndExp {
                    handle_equal_types($1, $3);
                    $$ = $1; // Assume AND expressions yield the same type
                }
                | NotExp {
                    $$ = $1;
                }
;

NotExp: NOT CompareExp {
                    $$ = $2;                 
                }
                | CompareExp {
                    $$ = $1;
                }
;

CompareExp: AddExp '=' CompareExp {
                    handle_non_numeric($1);
                    handle_non_numeric($3);
                    handle_equal_types($1, $3);
                    $$ = "int"; // Comparison yields boolean type
                }
                | AddExp NOT_EQUAL_TO_A CompareExp {
                    handle_non_numeric($1);
                    handle_non_numeric($3);
                    handle_equal_types($1, $3);
                    $$ = "int"; // Comparison yields boolean type
                }
                | AddExp NOT_EQUAL_TO_B CompareExp {
                    handle_non_numeric($1);
                    handle_non_numeric($3);
                    handle_equal_types($1, $3);
                    $$ = "int"; // Comparison yields boolean type
                }
                | AddExp '>' CompareExp {
                    handle_non_numeric($1);
                    handle_non_numeric($3);
                    handle_equal_types($1, $3);
                    $$ = "int"; // Comparison yields boolean type
                }
                | AddExp GREATER_OR_EQUAL_THAN CompareExp {
                    handle_non_numeric($1);
                    handle_non_numeric($3);
                    handle_equal_types($1, $3);
                    $$ = "int"; // Comparison yields boolean type
                }
                | AddExp '<' CompareExp {
                    handle_non_numeric($1);
                    handle_non_numeric($3);
                    handle_equal_types($1, $3);
                    $$ = "int"; // Comparison yields boolean type
                }
                | AddExp LESS_OR_EQUAL_THAN CompareExp {
                    handle_non_numeric($1);
                    handle_non_numeric($3);
                    handle_equal_types($1, $3);
                    $$ = "int"; // Comparison yields boolean type
                }
                | AddExp {
                    $$ = $1;
                }
;

AddExp: MultExp '+' AddExp {
                    handle_arithmetic_types($1, $3);
                    $$ = $1; // Assume result type is same as operands
                }
                | MultExp '-' AddExp {
                    handle_arithmetic_types($1, $3);
                    $$ = $1; // Assume result type is same as operands
                }
                | MultExp {
                    $$ = $1;
                }
;

MultExp: NegateExp '*' MultExp {
                    handle_arithmetic_types($1, $3);
                    $$ = $1; // Assume result type is same as operands
                }
                | NegateExp '/' MultExp {
                    handle_arithmetic_types($1, $3);
                    $$ = $1; // Assume result type is same as operands
                }
                | NegateExp {
                    $$ = $1;
                }
;

NegateExp: '-' PowerExp {
                    $$ = $2;
                }
                | PowerExp {
                    $$ = $1;
                }
;

PowerExp: Value PowerExp2 {
                    $$ = $1; // Assume result type is same as base
                }
                | Value {
                    $$ = $1;
                }
;

PowerExp2: '^' PowerExp {
                    handle_non_numeric($2);
                    $$ = $2;
                }
;

Value: '(' Expression ')' {
                    $$ = $2;                
                }
                | ID {
                    if(check_if_variable_is_declared($1)){
                        $$ = get_variable_type($1);
                    } else {
                        yyerror("Semantic error - Variable used before declaration.");
                        $$ = "unknown";
                    }
                }
                | ID '(' ExpressionList ')' {
                    if(check_if_variable_is_declared($1)){
                        $$ = get_variable_type($1);
                    } else {
                        yyerror("Semantic error - Variable used before declaration.");
                        $$ = "unknown";
                    }
                }
                | Constant {
                    $$ = $1;
                }
;

Constant: Integer {
                $$ = "int";
            }
             | String {
                $$ = "string";
            }
             | Real {
                $$ = "float";
            }
%%

int main(){
    yyin = stdin;

    do {
        yyparse();
    } while(!feof(yyin));

    return 0;
}

void yyerror(const char* s){
    fprintf(stderr, "Parse error: %s\n", s);
    exit(1);
}
