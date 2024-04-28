GRAMMAR_TABLE = {}
# TODO: converter first_follow.py pra gramática no formato abaixo
"""
<Lines>       ::= Integer <Statements> NewLine <Lines> 
                | Integer <Statements> NewLine

<Statements>  ::= <Statement> ':' <Statements>
                | <Statement>

<Statement>   ::= CLOSE '#' Integer
                | DATA <Constant List> 
                | DIM ID '(' <Integer List> ')'
                | END          
                | FOR ID '=' <Expression> TO <Expression>     
                | FOR ID '=' <Expression> TO <Expression> STEP Integer      
                | GOTO <Expression> 
                | GOSUB <Expression> 
                | IF <Expression> THEN <Statement>         
                | INPUT <ID List>       
                | INPUT '#' Integer ',' <ID List>       
                | LET Id '=' <Expression> 
                | NEXT <ID List>               
                | OPEN <Value> FOR <Access> AS '#' Integer
                | POKE <Value List>
                | PRINT <Print list>
                | PRINT '#' Integer ',' <Print List>
                | READ <ID List>           
                | RETURN
                | RESTORE
                | RUN
                | STOP
                | SYS <Value>
                | WAIT <Value List>
                | Remark

<Access>   ::= INPUT
             | OUPUT
                   
<ID List>  ::= ID ',' <ID List> 
             | ID 

<Value List>      ::= <Value> ',' <Value List> 
                    | <Value> 

<Constant List>   ::= <Constant> ',' <Constant List> 
                    | <Constant> 

<Integer List>    ::= Integer ',' <Integer List>
                    | Integer
                 
<Expression List> ::= <Expression> ',' <Expression List> 
                    | <Expression> 

<Print List>      ::= <Expression> ';' <Print List>
                    | <Expression> 
                    |  

<Expression>  ::= <And Exp> OR <Expression> 
                | <And Exp> 

<And Exp>     ::= <Not Exp> AND <And Exp> 
                | <Not Exp> 
 
<Not Exp>     ::= NOT <Compare Exp> 
                | <Compare Exp> 

<Compare Exp> ::= <Add Exp> '='  <Compare Exp> 
                | <Add Exp> '<>' <Compare Exp> 
                | <Add Exp> '><' <Compare Exp> 
                | <Add Exp> '>'  <Compare Exp> 
                | <Add Exp> '>=' <Compare Exp> 
                | <Add Exp> '<'  <Compare Exp> 
                | <Add Exp> '<=' <Compare Exp> 
                | <Add Exp> 

<Add Exp>     ::= <Mult Exp> '+' <Add Exp> 
                | <Mult Exp> '-' <Add Exp> 
                | <Mult Exp> 

<Mult Exp>    ::= <Negate Exp> '*' <Mult Exp> 
                | <Negate Exp> '/' <Mult Exp> 
                | <Negate Exp> 

<Negate Exp>  ::= '-' <Power Exp> 
                | <Power Exp> 

<Power Exp>   ::= <Value> <Power Exp'> 
                | <Value>

<Power Exp'>   ::= '^' <Power Exp>

<Value>       ::= '(' <Expression> ')'
                | ID 
                | ID '(' <Expression List> ')'
                | <Constant> 

<Constant> ::= Integer 
             | String 
             | Real 
"""