/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_TAB_H_INCLUDED
# define YY_YY_PARSER_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 1
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    Integer = 258,                 /* Integer  */
    String = 259,                  /* String  */
    Real = 260,                    /* Real  */
    NewLine = 261,                 /* NewLine  */
    ID = 262,                      /* ID  */
    CLOSE = 263,                   /* CLOSE  */
    DATA = 264,                    /* DATA  */
    DIM = 265,                     /* DIM  */
    END = 266,                     /* END  */
    FOR = 267,                     /* FOR  */
    GOTO = 268,                    /* GOTO  */
    GOSUB = 269,                   /* GOSUB  */
    IF = 270,                      /* IF  */
    INPUT = 271,                   /* INPUT  */
    LET = 272,                     /* LET  */
    NEXT = 273,                    /* NEXT  */
    OPEN = 274,                    /* OPEN  */
    POKE = 275,                    /* POKE  */
    PRINT = 276,                   /* PRINT  */
    READ = 277,                    /* READ  */
    RETURN = 278,                  /* RETURN  */
    RESTORE = 279,                 /* RESTORE  */
    RUN = 280,                     /* RUN  */
    STOP = 281,                    /* STOP  */
    SYS = 282,                     /* SYS  */
    WAIT = 283,                    /* WAIT  */
    Remark = 284,                  /* Remark  */
    TO = 285,                      /* TO  */
    STEP = 286,                    /* STEP  */
    AS = 287,                      /* AS  */
    THEN = 288,                    /* THEN  */
    OUTPUT = 289,                  /* OUTPUT  */
    OR = 290,                      /* OR  */
    AND = 291,                     /* AND  */
    NOT = 292,                     /* NOT  */
    Branco = 293,                  /* Branco  */
    NOT_EQUAL_TO_A = 294,          /* "<>"  */
    NOT_EQUAL_TO_B = 295,          /* "><"  */
    GREATER_OR_EQUAL_THAN = 296,   /* ">="  */
    LESS_OR_EQUAL_THAN = 297       /* "<="  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 58 "parser.y"

    int ival; // For integers
    char* sval; // For strings like identifiers

#line 111 "parser.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_PARSER_TAB_H_INCLUDED  */
