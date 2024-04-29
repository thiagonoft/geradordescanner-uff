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
 
SPECIAL_CHARS = "+,)(.*"
class State:
    def __init__(self, is_final=False):
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
        self.states = [start_state]
 
    def add_state(self, state):
        self.states.append(state)

    def merge_nfa(self, other_nfa):
        for state in other_nfa.states:
            self.add_state(state)
 
 
def pop_until_open_parenthesis(exp_stack):
    """
    Desempilha caracteres até encontrar o parêntese aberto correspondente,
    considerando aninhamento de parênteses. Retorna a expressão desempilhada como uma string.
    """
    nested = 0  # Para controlar parênteses aninhados
    expr = []
 
    while exp_stack:
        char = exp_stack.pop()
        if char == '(':
            nested -= 1
            if nested == 0:
                break
        elif char == ')':
            nested += 1
        expr.append(char)
 
    # Retorna a expressão desempilhada e invertida, pois a desempilhamos em ordem reversa
    return ''.join(reversed(expr))
 
 
def process_plus_operator(exp_stack):
    # Processa o operador '+'
    expression = pop_until_open_parenthesis(exp_stack)
    expression_elements = [c for c in expression if c not in SPECIAL_CHARS]

    # Cria o estado inicial do NFA
    initial_state = State()
    nfa = NFA(initial_state)
    current_state = initial_state

    # Cria estados e transições para cada elemento na expressão
    for i, element in enumerate(expression_elements):
        next_state = State()
        current_state.add_transition(element, next_state)
        nfa.add_state(next_state)
        current_state = next_state

    # Faz o último estado apontar para o primeiro e marca como final
    current_state.add_transition('ε', initial_state)
    current_state.is_final = True
 
    return nfa
 
 
def process_concatenation(exp_stack):
    # Processa a concatenação
    expression = pop_until_open_parenthesis(exp_stack)
    expression_elements = [c for c in expression if c not in SPECIAL_CHARS]
 
    S1 = State()
    S2 = State()
    S3 = State(is_final=True)
 
    S1.add_transition(expression_elements[0], S2)
    S2.add_transition(expression_elements[1], S3)
 
    nfa = NFA(S1)
    nfa.add_state(S1)
    nfa.add_state(S2)
    nfa.add_state(S3)
 
    return nfa
 
 
def process_union(exp_stack):
    # Processa a união
    expression = pop_until_open_parenthesis(exp_stack)
    expression_elements = [c for c in expression if c not in SPECIAL_CHARS]
 
    S1 = State()
    S2 = State()
    S3 = State()
    S4 = State(is_final=True)
 
    S1.add_transition('ε', S2)
    S1.add_transition('ε', S3)
    S2.add_transition(expression_elements[0], S4)
    S3.add_transition(expression_elements[1], S4)
 
    nfa = NFA(S1)
    nfa.add_state(S1)
    nfa.add_state(S2)
    nfa.add_state(S3)
    nfa.add_state(S4)
 
    return nfa
 
 
def process_kleene_closure(exp_stack):
    # Processa o fecho de Kleene
    expression = pop_until_open_parenthesis(exp_stack)
    expression_elements = [c for c in expression if c not in SPECIAL_CHARS]

    # Cria um estado inicial que também é o estado final (aceitação)
    initial_state = State(is_final=True)
    current_state = initial_state

    # Cria um NFA com o estado inicial
    nfa = NFA(initial_state)

    # Loop para adicionar estados e transições para cada elemento na expressão
    for element in expression_elements:
        next_state = State()
        current_state.add_transition(element, next_state)
        nfa.add_state(next_state)
        current_state = next_state

    # Adiciona transição epsilon do último estado para o estado inicial
    current_state.add_transition('ε', initial_state)

    return nfa
 
def process_optional(exp_stack):
    # Processa o símbolo opcional
    expression = pop_until_open_parenthesis(exp_stack)
    expression_elements = [c for c in expression if c not in SPECIAL_CHARS]
 
    S1 = State()
    S2 = State(is_final=True)
 
    S1.add_transition('ε', S2)
    S1.add_transition(expression_elements[0], S2)
 
    nfa = NFA(S1)
    nfa.add_state(S1)
    nfa.add_state(S2)
 
    return nfa

def process_character_set(expression, exp_stack):
    # Assume que a expressão vem no formato [a-z] ou [abc]
    # Primeiro, removemos os colchetes
    content = expression[1:-1]
    
    start_state = State()
    final_state = State(is_final=True)

    if '-' in content:  # Verifica se é um intervalo
        start_char, end_char = content.split('-')
        start_state.add_range_transitions(start_char, end_char, final_state)
    else:  # Trata-se de caracteres individuais
        for char in content:
            start_state.add_transition(char, final_state)

    nfa = NFA(start_state)
    nfa.add_state(start_state)
    nfa.add_state(final_state)
    return nfa
 
def print_nfa(nfa):
    # Cria um mapeamento completo de todos os estados acessíveis a partir do estado inicial
    state_index = {}
    states_to_process = [nfa.start_state]
    index = 0

    # Uso de BFS para mapear todos os estados com índices únicos
    while states_to_process:
        current_state = states_to_process.pop(0)
        if current_state not in state_index:
            state_index[current_state] = index
            index += 1
            # Adiciona estados de transições simbólicas ao BFS queue
            for symbol_transitions in current_state.transitions.values():
                for state in symbol_transitions:
                    if state not in state_index:
                        states_to_process.append(state)
            # Adiciona estados de transições epsilon ao BFS queue
            for state in current_state.episilon_transitions:
                if state not in state_index:
                    states_to_process.append(state)

    # Imprime as transições de cada estado
    print("NFA:")
    for state in state_index:
        state_idx = state_index[state]
        print(f'Transições do estado {state_idx}:')
        for symbol, transitions in state.transitions.items():
            for transition in transitions:
                transition_idx = state_index[transition]
                print(f"  Símbolo: {symbol}, Vai para: Estado {transition_idx}")
        for transition in state.episilon_transitions:
            transition_idx = state_index[transition]
            print(f"  Símbolo: ε, Vai para: Estado {transition_idx}")

def add_epsilon_transitions_between_nfas(nfas):
    combined_nfa = nfas[0]  # Começa com o primeiro NFA

    for i in range(len(nfas) - 1):
        current_nfa = nfas[i]
        next_nfa = nfas[i + 1]

        final_states_current = [state for state in current_nfa.states if state.is_final]
        start_state_next = next_nfa.start_state

        # Adicionar transições epsilon dos estados finais do NFA atual para o estado inicial do próximo NFA
        for final_state in final_states_current:
            if start_state_next not in final_state.episilon_transitions:
                final_state.add_transition('ε', start_state_next)

        # Agora, adicione todos os estados do próximo NFA ao NFA combinado
        combined_nfa.merge_nfa(next_nfa)

    return combined_nfa

def scan_expression(exp: str):
    exp_splitted = list(exp)
    exp_stack = []
    nfas = []
    skip_until_index = -1 # Para controlar a captura de conjuntos de caracteres
 
    for i, c in enumerate(exp_splitted):
        print(exp_stack)
        if i < skip_until_index:
            # Se estivermos em um índice que deve ser pulado, continue para a próxima iteração
            continue
        if c == '[':
            # Inicia a captura do conjunto de caracteres
            start_index = i
            while exp_splitted[i] != ']':
                i += 1
            # Captura o conteúdo entre os colchetes, inclusive
            char_set = ''.join(exp_splitted[start_index:i+1])
            nfa = process_character_set(char_set, exp_stack)  # Processa o conjunto de caracteres
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
            skip_until_index = i + 1  # Atualiza o índice até o qual devemos pular
        if c == '+':
            nfa = process_plus_operator(exp_stack)  # Fecho Positivo
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        elif c == '~':
            nfa = process_concatenation(exp_stack)  # Concatenação
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        elif c == '|':  # União
            nfa = process_union(exp_stack)
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        elif c == '*':
            nfa = process_kleene_closure(exp_stack)
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        elif c == '?':
            nfa = process_optional(exp_stack)  # Símbolo opcional
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        else:
            exp_stack.append(c)
 
    nfa_final = add_epsilon_transitions_between_nfas(nfas)
    # print(exp_splitted)
    print(exp_stack)


    print_nfa(nfa_final)


    return exp
 
 
scan_expression("(ab)+(7)*(@)+")