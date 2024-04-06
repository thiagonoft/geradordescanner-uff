# *(.(+(a,b),+(a,E)))
""" 
Concatenação: A sequência simples de caracteres um após o outro representa a concatenação. Por exemplo, a expressão regular ab corresponde à sequência "ab".

União ou alternância (|): Representa a escolha entre dois ou mais padrões. Por exemplo, a|b corresponde a "a" ou "b".

Fecho de Kleene (*): Indica que o símbolo anterior pode ser repetido zero ou mais vezes. Por exemplo, a* corresponde a "", "a", "aa", "aaa", etc.

Fecho positivo (+): Similar ao fecho de Kleene, mas o símbolo anterior deve aparecer pelo menos uma vez. Por exemplo, a+ corresponde a "a", "aa", "aaa", etc., mas não a "".

Opcional (?): Indica que o símbolo anterior pode aparecer zero ou uma vez. Por exemplo, a? corresponde a "" ou "a".

Conjuntos de caracteres ([ ]): Especificam um conjunto de caracteres dos quais qualquer um pode ser aceito. Por exemplo, [abc] corresponde a "a", "b", ou "c". Intervalos podem ser especificados usando um hífen, como em [a-z] para qualquer letra minúscula.

Negação (^): Quando usado dentro de um conjunto de caracteres, nega o conjunto. Por exemplo, [^a] corresponde a qualquer caractere exceto "a".

Grupos e subpadrões ( ): Agrupam partes de uma expressão regular, permitindo que você aplique operadores como * ou + a um grupo inteiro. Por exemplo, (ab)+ corresponde a "ab", "abab", "ababab", etc.

Ancoragem:

Início de linha (^): Quando usado fora de um conjunto de caracteres, corresponde ao início de uma linha.
Fim de linha ($): Corresponde ao final de uma linha.
Por exemplo, ^a corresponde a qualquer "a" no início de uma linha, e a$ corresponde a "a" no final de uma linha.
Escape (\): Usado para escapar caracteres especiais, permitindo que sejam tratados como caracteres comuns. Por exemplo, \\. corresponde a um ponto literal, em vez de qualquer caractere."""
 
class State:
    def __init__(self, is_final= False):
        self.is_final = is_final
        self.transitions = {}
        self.episilon_transitions = []
 
    def add_transition(self, symbol, next_state):
        if symbol == 'ε':
            self.episilon_transitions.append(next_state)
 
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(next_state)
 
    def add_range_transitions(self, start_char, end_char, state):
        for ascii_code in range(ord(start_char), ord(end_char) + 1):
            self.add_transition(chr(ascii_code), state)
 
class NFA:
    def __init__(self, start_state):
        self.start_state = start_state
 
def scan_expression(exp: str):
    exp_splitted = list(exp)
    exp_stack = []
    processed_exps = []
 
    curr_state = State()
    next_state = State()
    nfa = NFA(curr_state)
    special_chars = "+,)(.*"
 
    for i, c in enumerate(exp_splitted):
        if c == '+':
            back_count = 0
            while exp_splitted[i - back_count] != '(':
                exp_stack.append(exp_splitted[i - back_count])
                back_count += 1
            exp_stack.append(exp_splitted[i - back_count])
            print(exp_stack)
 
            for stack_member in exp_stack:
                #
                if stack_member not in special_chars:
                    curr_state.add_transition(stack_member, State())
 
            # print("curr_state", curr_state)
            # print("curr_state.transitions", curr_state.transitions)
            # print("nfa.start_state", nfa.start_state)
            # print("nfa.start_state.transitions", nfa.start_state.transitions)
            # print("exp_stack", exp_stack)
 
            curr_state = next_state
            next_state = State()
 
 
            break
 
    # print(exp_splitted)
    return exp
 
scan_expression("(a,b)+,(a,ε)+")