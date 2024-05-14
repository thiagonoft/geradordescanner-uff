# fonte: https://github.com/PranayT17/Finding-FIRST-and-FOLLOW-of-given-grammar/blob/master/first_follow.py
import sys
import json

sys.setrecursionlimit(60)

# Opening JSON file
with open('/home/gustavo/Projects/geradordescanner-uff/parser/symbols_dict.json') as json_file:
    symbols_conversion = json.load(json_file)

def first(string):
    #print("first({})".format(string))
    first_ = set()
    if string in non_terminals:
        alternatives = productions_dict[string]

        for alternative in alternatives:
            first_2 = first(alternative)
            first_ = first_ |first_2

    elif string in terminals:
        first_ = {string}

    elif string=='' or string=='@':
        first_ = {'@'}

    else:
        first_2 = first(string[0])
        if '@' in first_2:
            i = 1
            while '@' in first_2:
                #print("inside while")

                first_ = first_ | (first_2 - {'@'})
                #print('string[i:]=', string[i:])
                if string[i:] in terminals:
                    first_ = first_ | {string[i:]}
                    break
                elif string[i:] == '':
                    first_ = first_ | {'@'}
                    break
                first_2 = first(string[i:])
                first_ = first_ | first_2 - {'@'}
                i += 1
        else:
            first_ = first_ | first_2


    #print("returning for first({})".format(string),first_)
    return  first_


def follow(nT):
    #print("inside follow({})".format(nT))
    follow_ = set()
    #print("FOLLOW", FOLLOW)
    prods = productions_dict.items()
    if nT==starting_symbol:
        follow_ = follow_ | {'$'}
    
    for nt,rhs in prods:
        #print("nt to rhs", nt,rhs)
        for alt in rhs:
            for char in alt:
                if char==nT:
                    following_str = alt[alt.index(char) + 1:]
                    if following_str=='':
                        if nt==nT:
                            continue
                        else:
                            if char not in "€†q":
                                follow_ = follow_ | follow(nt)
                                print(f"nt={nt}, ({symbols_conversion[nt]})")
                    else:
                        follow_2 = first(following_str)
                        if '@' in follow_2:
                            follow_ = follow_ | follow_2-{'@'}
                            follow_ = follow_ | follow(nt)
                        else:
                            follow_ = follow_ | follow_2
    #print("returning for follow({})".format(nT),follow_)
    return follow_


no_of_terminals=54
terminals_str = """C
Y
'
]
;
c
~
j
&
W
)
k
¨
,
(
X
s
U
M
%
?
.
F
T
*
i
o
m
P
R
G
g
h
{
e
`
L
O
l
+
<
u
v
}
I
n
[
Q
S
A
:
J
=
b"""
terminals = terminals_str.split("\n")
no_of_non_terminals=23
non_terminals_str ="""q
B
€
N
a
y
w
r
D
E
f
t
p
†
K
x
!
z
H
V
d
#
Z"""
non_terminals = non_terminals_str.split("\n")
starting_symbol = "D"
no_of_productions = 23
productions_str ="""D->ABCD/ABC
B->E¨B/E
E->F&A/GH/IJ*K(/L/MJ)NON/MJ)NONPA/QN/RN/SNTE/UV/U&A<V/WJ)N/XV/YZMab&A/cd/ef/e&A<f/gV/h/i/j/k/lZ/md/n
a->U/o
V->J€
€-><JV/@
d->Z<d/Z
H->p<H/p
K->A†
†-><AK/@
q->N<q/N
f->N'f/N/~
N->rsN/r
r->tur/t
t->vw/w
w->x)w/x+w/x=w/x.w/x,w/x:w/x;w/x
x->y?x/y[x/y
y->z]y/z{y/z
z->[!/!
!->Z#/Z
#->}!/@
Z->*N(/J/J*q(/p
p->A/`/%"""
productions = productions_str.split("\n")

productions_dict = {}

for nT in non_terminals:
    productions_dict[nT] = []

for production in productions:
    nonterm_to_prod = production.split("->")
    alternatives = nonterm_to_prod[1].split("/")
    for alternative in alternatives:
        productions_dict[nonterm_to_prod[0]].append(alternative)

#print("productions_dict",productions_dict)
#print("nonterm_to_prod",nonterm_to_prod)
#print("alternatives",alternatives)


FIRST = {}
FOLLOW = {}

for non_terminal in non_terminals:
    FIRST[non_terminal] = set()

for non_terminal in non_terminals:
    FOLLOW[non_terminal] = set()

#print("FIRST",FIRST)

for non_terminal in non_terminals:
    FIRST[non_terminal] = FIRST[non_terminal] | first(non_terminal)

print("FIRST",FIRST)


# FIRST = {'q': {'`', 'A', 'J', '*', '[', '%', 'v'}, 'B': {'I', 'j', 'U', 'S', 'h', 'G', 'k', 'F', 'i', 'l', 'M', 'n', 'R', 'Q', 'm', 'e', 'X', 'L', 'g', 'W', 'c', 'Y'}, '€': {'<', '@'}, 'N': {'`', 'A', 'J', '*', '[', '%', 'v'}, 'a': {'o', 'U'}, 'y': {'`', 'A', 'J', '*', '[', '%'}, 'w': {'`', 'A', 'J', '*', '[', '%'}, 'r': {'`', 'A', 'J', '*', '[', '%', 'v'}, 'D': {'A'}, 'E': {'I', 'U', 'j', 'S', 'h', 'G', 'k', 'F', 'i', 'M', 'l', 'n', 'Q', 'R', 'e', 'm', 'X', 'L', 'g', 'W', 'c', 'Y'}, 'f': {'A', '*', 'v', '`', 'J', '[', '%', '~'}, 't': {'`', 'A', 'J', '*', '[', '%', 'v'}, 'p': {'`', '%', 'A'}, '†': {'<', '@'}, 'K': {'A'}, 'x': {'`', 'A', 'J', '*', '[', '%'}, '!': {'`', 'A', 'J', '*', '%'}, 'z': {'`', 'A', 'J', '*', '[', '%'}, 'H': {'`', '%', 'A'}, 'V': {'J'}, 'd': {'`', 'A', 'J', '*', '%'}, '#': {'}', '@'}, 'Z': {'`', 'A', 'J', '*', '%'}}

# input("")

# TODO: follow iterativo

FOLLOW[starting_symbol] = FOLLOW[starting_symbol] | {'$'}
for non_terminal in non_terminals:
    FOLLOW[non_terminal] = FOLLOW[non_terminal] | follow(non_terminal)

#print("FOLLOW", FOLLOW)

print("{: ^20}{: ^20}{: ^20}".format('Non Terminals','First','Follow'))
for non_terminal in non_terminals:
    print("{: ^20}{: ^20}{: ^20}".format(non_terminal,str(FIRST[non_terminal]),str(FOLLOW[non_terminal])))