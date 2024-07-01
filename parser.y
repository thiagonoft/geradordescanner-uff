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
    struct {
        char* type;
        char* code;
    } attrib;
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

%type <attrib> Constant Expression AndExp NotExp CompareExp AddExp MultExp NegateExp PowerExp PowerExp2 Value
%type <attrib> Statement Statements PrintList ExpressionList IDList IntegerList ConstantList ValueList
/* 
 */

%%

Lines: Integer Statements NewLine Lines {
                    printf("%s\n", $2.code);
                }
                | Integer Statements NewLine {
                    printf("%s\n", $2.code);
                }
;

Statements: Statement ':' Statements {
                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 2);
                    sprintf(expr, "%s\n%s", $1.code, $3.code);
                    $$.code = expr;
                }
                | Statement {
                    $$.code = $1.code;
                }
;

Statement: CLOSE '#' Integer {
                    $$.code = strdup("");
                }
                | DATA ConstantList {
                    $$.code = strdup("");
                }
                | DIM ID '(' IntegerList ')' {
                    declare_variable_on_let($2, "int");
                }
                | END {
                    $$.code = strdup("");
                }
                | FOR ID '=' Expression TO Expression {
                    declare_variable_on_for($2);

                    char* expr = (char*)malloc(strlen($2) + strlen($4.code) + strlen($6.code) + 30);
                    sprintf(expr, "for %s in range(%s, %s + 1):", $2, $4.code, $6.code);
                    $$.code = expr;
                }
                | FOR ID '=' Expression TO Expression STEP Integer {
                    declare_variable_on_for($2);

                    $$.code = strdup("");
                }
                | GOTO Expression {
                    $$.code = strdup("");
                }
                | GOSUB Expression {
                    $$.code = strdup("");
                }
                | IF Expression THEN Statement {
                    $$.code = strdup("");
                }
                | INPUT IDList {
                    $$.code = strdup("");
                }
                | INPUT '#' Integer ',' IDList {
                    $$.code = strdup("");
                }
                | LET ID '=' Expression {
                    declare_variable_on_let($2, $4.type);

                    char* expr = (char*)malloc(strlen($2) + strlen($4.code) + 10);
                    sprintf(expr, "%s = %s", $2, $4.code);
                    $$.code = expr;
                }
                | NEXT IDList {
                    $$.code = strdup("");
                }
                | OPEN Value FOR Access AS '#' Integer {
                    $$.code = strdup("");
                }
                | POKE ValueList {
                    $$.code = strdup("");
                }
                | PRINT PrintList {
                    char* expr = (char*)malloc(strlen($2.code) + 20);
                    sprintf(expr, "print(%s)", $2.code);
                    $$.code = expr;
                }
                | PRINT '#' Integer ',' PrintList {
                    $$.code = strdup("");
                }
                | READ IDList {
                    $$.code = strdup("");
                }
                | RETURN {
                    $$.code = strdup("");
                }
                | RESTORE {
                    $$.code = strdup("");
                }
                | RUN {
                    $$.code = strdup("");
                }
                | STOP {
                    $$.code = strdup("");
                }
                | SYS Value {
                    $$.code = strdup("");
                }
                | WAIT ValueList {
                    $$.code = strdup("");
                }
                | Remark {
                    $$.code = strdup("");
                }
;

Access: INPUT
             | OUTPUT
;

IDList: ID ',' IDList {
                char* expr = (char*)malloc(strlen($1) + strlen($3.code) + 3);
                sprintf(expr, "%s, %s", $1, $3.code);
                $$.code = expr;
            }
             | ID {
                $$.code = $1;
             }
;

ValueList: Value ',' ValueList
                | Value {
                    $$.code = $1.code;
                }
;

ConstantList: Constant ',' ConstantList
                | Constant {
                    $$.code = $1.code;
                }
;

IntegerList: Integer ',' IntegerList {
                    char* expr = (char*)malloc(20);
                    sprintf(expr, "%d, %s", $1, $3.code);
                    $$.code = expr;   
                    }
                    | Integer {
                        char* expr = (char*)malloc(20);
                        sprintf(expr, "%d", $1);
                        $$.code = expr;
                    }
;

ExpressionList: Expression ',' ExpressionList {
                        char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 3);
                        sprintf(expr, "%s, %s", $1.code, $3.code);
                        $$.code = expr;
                    }
                    | Expression {
                        $$.code = $1.code;
                    }
;

PrintList: Expression ';' PrintList {
                        char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 3);
                        sprintf(expr, "%s; %s", $1.code, $3.code);
                        $$.code = expr;
                    }
                    | Expression {
                        $$.code = $1.code;
                    }
                    | Branco {
                        $$.code = strdup("");
                    }
;

Expression: AndExp OR Expression {
                    handle_equal_types($1.type, $3.type);
                    $$.type = $1.type; // Assume OR expressions yield the same type

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s or %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | AndExp {
                    $$.type = $1.type;
                    $$.code = $1.code;
                }
;

AndExp: NotExp AND AndExp {
                    handle_equal_types($1.type, $3.type);
                    $$.type = $1.type; // Assume AND expressions yield the same type

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s and %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | NotExp {
                    $$.type = $1.type;
                    $$.code = $1.code;
                }
;

NotExp: NOT CompareExp {
                    $$.type = $2.type; 
                    char* expr = (char*)malloc(strlen($2.code) + 10);
                    sprintf(expr, "not %s", $2.code);
                    $$.code = expr;                
                }
                | CompareExp {
                    $$.type = $1.type;
                    $$.code = $1.code;
                }
;

CompareExp: AddExp '=' CompareExp {
                    handle_non_numeric($1.type);
                    handle_non_numeric($3.type);
                    handle_equal_types($1.type, $3.type);
                    $$.type = "int"; // Comparison yields boolean type
                    
                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s == %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | AddExp NOT_EQUAL_TO_A CompareExp {
                    handle_non_numeric($1.type);
                    handle_non_numeric($3.type);
                    handle_equal_types($1.type, $3.type);
                    $$.type = "int"; // Comparison yields boolean type

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s != %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | AddExp NOT_EQUAL_TO_B CompareExp {
                    handle_non_numeric($1.type);
                    handle_non_numeric($3.type);
                    handle_equal_types($1.type, $3.type);
                    $$.type = "int"; // Comparison yields boolean type

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s != %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | AddExp '>' CompareExp {
                    handle_non_numeric($1.type);
                    handle_non_numeric($3.type);
                    handle_equal_types($1.type, $3.type);
                    $$.type = "int"; // Comparison yields boolean type

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s > %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | AddExp GREATER_OR_EQUAL_THAN CompareExp {
                    handle_non_numeric($1.type);
                    handle_non_numeric($3.type);
                    handle_equal_types($1.type, $3.type);
                    $$.type = "int"; // Comparison yields boolean type

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s >= %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | AddExp '<' CompareExp {
                    handle_non_numeric($1.type);
                    handle_non_numeric($3.type);
                    handle_equal_types($1.type, $3.type);
                    $$.type = "int"; // Comparison yields boolean type

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s < %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | AddExp LESS_OR_EQUAL_THAN CompareExp {
                    handle_non_numeric($1.type);
                    handle_non_numeric($3.type);
                    handle_equal_types($1.type, $3.type);
                    $$.type = "int"; // Comparison yields boolean type

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s <= %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | AddExp {
                    $$.type = $1.type;
                    $$.code = $1.code;
                }
;

AddExp: MultExp '+' AddExp {
                    handle_arithmetic_types($1.type, $3.type);
                    $$.type = $1.type; // Assume result type is same as operands

                    printf("DEBUG: %s\n", $3.code);
                    printf("DEBUG2: %s\n", $1.code);

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s + %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | MultExp '-' AddExp {
                    handle_arithmetic_types($1.type, $3.type);
                    $$.type = $1.type; // Assume result type is same as operands

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s - %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | MultExp {
                    $$.type = $1.type;
                    $$.code = $1.code;
                }
;

MultExp: NegateExp '*' MultExp {
                    handle_arithmetic_types($1.type, $3.type);
                    $$.type = $1.type; // Assume result type is same as operands

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s * %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | NegateExp '/' MultExp {
                    handle_arithmetic_types($1.type, $3.type);
                    $$.type = $1.type; // Assume result type is same as operands

                    char* expr = (char*)malloc(strlen($1.code) + strlen($3.code) + 10);
                    sprintf(expr, "(%s / %s)", $1.code, $3.code);
                    $$.code = expr;
                }
                | NegateExp {
                    $$.type = $1.type;
                    $$.code = $1.code;
                }
;

NegateExp: '-' PowerExp {
                    $$.type = $2.type;

                    char* expr = (char*)malloc(strlen($2.code) + 10);
                    sprintf(expr, "-%s", $2.code);
                    $$.code = expr;
                }
                | PowerExp {
                    $$.type = $1.type;
                    $$.code = $1.code;
                }
;

PowerExp: Value PowerExp2 {
                    $$.type = $1.type; // Assume result type is same as base

                    char* expr = (char*)malloc(strlen($1.code) + strlen($2.code) + 10);
                    sprintf(expr, "(%s ** %s)", $1.code, $2.code);
                    $$.code = expr;
                }
                | Value {
                    $$.type = $1.type;
                    $$.code = $1.code;
                }
;

PowerExp2: '^' PowerExp {
                    handle_non_numeric($2.type);
                    $$.type = $2.type;

                    $$.code = $2.code;
                }
;

Value: '(' Expression ')' {
                    $$.type = $2.type;
                    $$.code = $2.code;                
                }
                | ID {
                    if(check_if_variable_is_declared($1)){
                        $$.type = get_variable_type($1);
                        $$.code = $1;
                    } else {
                        yyerror("Semantic error - Variable used before declaration.");
                    }
                }
                | ID '(' ExpressionList ')' {
                    if(check_if_variable_is_declared($1)){
                        $$.type = get_variable_type($1);
                    } else {
                        yyerror("Semantic error - Variable used before declaration.");
                    }
                }
                | Constant {
                    $$.type = $1.type;
                    $$.code = $1.code;
                }
;

Constant: Integer {
                $$.type = "int";

                char* const_val = (char*)malloc(20);
                sprintf(const_val, "%d", $1);
                $$.code = const_val;
            }
             | String {
                $$.type = "string";
                $$.code = $1;
            }
             | Real {
                $$.type = "float";

                char* const_val = (char*)malloc(20);
                sprintf(const_val, "%f", $1);
                $$.code = const_val;
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
