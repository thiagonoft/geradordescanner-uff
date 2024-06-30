%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Symbol {
    char* name;
    char* type; // "int", "float", etc.
    struct Symbol* next; // Para colisões em um possível hashing
} Symbol;

#define HASH_SIZE 101
static Symbol* symbol_table[HASH_SIZE];

// função hash
unsigned hash(char* str)
{
    unsigned hashval;
    for(hashval = 0;
        *str != '\0';
        str++)
    {
        hashval = *str + 31 * hashval;
    }
    return hashval % HASH_SIZE;
}

Symbol* lookup_symbol(char *name) {
    Symbol* sp;
    for(sp = symbol_table[hash(name)];
        sp != NULL;
        sp = sp->next)
    {
        if (strcmp(name, sp->name) == 0)
            return sp;
    }
    return NULL;
}

Symbol* insert_symbol(char *name, char *type) {
    unsigned hashval;
    Symbol* sp = lookup_symbol(name);
    if (sp == NULL)
    {
        sp = (Symbol*) malloc(sizeof(*sp));
        if (sp == NULL || (sp->name = strdup(name)) == NULL)
            return NULL;
        sp->type = strdup(type);
        hashval = hash(name);
        sp->next = symbol_table[hashval];
        symbol_table[hashval] = sp;
    }
    else
    {
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
void declare_variable_on_let(char* ID, char* type)
{
    Symbol* sym = lookup_symbol(ID);
    if (sym == NULL)
    {
        sym = insert_symbol(ID, type);
        if (sym == NULL)
        {
            yyerror("Memory error: could not declare variable");
        }
        else
        {
            printf("Variable %s explicitly set\n", ID);
        }
    }
    else
    {
        // lidar com a atribuição
        printf("Variable %s updated or redeclared\n", ID);
    }
}

void declare_variable_on_for(char* ID)
{
    Symbol* sym = lookup_symbol(ID);
    if (sym == NULL)
    {
        // Declaração implícita se não encontrada na tabela
        sym = insert_symbol(ID, "generic"); // Considera tipo genérico
        if (sym == NULL)
        {
            yyerror("Memory error: could not declare variable");
        }
        else
        {
            printf("Variable %s implicitly set\n", ID);
        }
    }
    else
    {
        printf("Variable %s is of type %s\n", ID, sym->type);
    }
}

bool check_if_variable_is_declared(char* ID)
{
    Symbol* sym = lookup_symbol(ID);
    if (sym == NULL)
    {
        // printf("Variable %s is not declared\n", ID);
        return false;
    }
    else
    {
        // printf("Variable %s is of type %s\n", ID, sym->type);
        return true;
    }
}

char* get_variable_type(char* ID) {
    Symbol* sym = lookup_symbol(ID);
    if (sym == NULL) {
        yyerror("Undeclared variable");
        return NULL;
    }
    return sym->type;
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
                | DIM ID '(' IntegerList ')'
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
                    printf("$4 = %s\n", $4);
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
                | AddExp NOT_EQUAL_TO_A CompareExp
                | AddExp NOT_EQUAL_TO_B CompareExp
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
                | ID {
                    bool declared = check_if_variable_is_declared($1);
                    if(declared)
                    {
                        char* varType = get_variable_type($1);
                        printf("Variable %s is of type %s\n", $1, varType);
                        $$ = varType;
                    }
                    else
                    {
                        yyerror("Semantic error - Variable used before declaration.");
                    } 
                }
                /* | ID '(' ExpressionList ')' */
                | Constant {
                    // printf("$$ = %s\n", $$);
                    $$ = $1;
                    // printf("$1 = %s\n", $1);
                }
;

Constant: Integer {
                $$ = "int";
                // printf("Integer: %d\n", $1);
            }
             | String {
                $$ = "string";
                // printf("String: %s\n", $1);
            }
            // MUDAR NO SCANNER PRA PEGAR REAL
             | Real {
                $$ = "float";
                // printf("float: %f\n", $1);
            }
%%

int main()
{
	yyin = stdin;

	do
    {
		yyparse();
	} while(!feof(yyin));

	return 0;
}

void yyerror(const char* s) {
	fprintf(stderr, "Parse error: %s\n", s);
	exit(1);
}