import re
import unicodedata

SPECIAL_CHARS = "+,)(.*"

class State:
    def __init__(self, is_final=False):
        self.is_final = is_final
        self.transitions = {}
        self.episilon_transitions = []

    def add_transition(self, symbol, next_state):
        if symbol == 'ε':
            self.episilon_transitions.append(next_state)
        else:
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
    nested = 0
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

    return ''.join(reversed(expr))


def process_plus_operator(exp_stack, nfas):
    expression = pop_until_open_parenthesis(exp_stack)
    expression_elements = [c for c in expression if c not in SPECIAL_CHARS]

    if 'NFA_' in expression:
        position = expression.find('_')
        nfa = nfas[int(expression[position+1:position+2])]
        final_state = [state for state in nfa.states if state.is_final]
        if final_state:
            final_state[0].add_transition('ε', nfa.start_state)
        nfas.pop(int(expression[position+1:position+2]))
    else:
        initial_state = State()
        nfa = NFA(initial_state)
        current_state = initial_state

        for i, element in enumerate(expression_elements):
            next_state = State()
            current_state.add_transition(element, next_state)
            nfa.add_state(next_state)
            current_state = next_state

        current_state.add_transition('ε', initial_state)
        current_state.is_final = True

    return nfa


def process_concatenation(exp_stack):
    expression = pop_until_open_parenthesis(exp_stack)
    expression_elements = [c for c in expression if c not in SPECIAL_CHARS]

    S1 = State()
    S2 = State()
    S3 = State(is_final=True)

    S1.add_transition(expression_elements[0], S2)
    S2.add_transition(expression_elements[1], S3)

    nfa = NFA(S1)
    nfa.add_state(S2)
    nfa.add_state(S3)

    return nfa


def process_union(exp_stack):
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
    nfa.add_state(S2)
    nfa.add_state(S3)
    nfa.add_state(S4)

    return nfa


def process_kleene_closure(exp_stack, nfas):
    expression = pop_until_open_parenthesis(exp_stack)
    expression_elements = [c for c in expression if c not in SPECIAL_CHARS]

    if 'NFA_' in expression:
        position = expression.find('_')
        nfa = nfas[int(expression[position+1:position + 2])]
        final_state = [state for state in nfa.states if state.is_final]
        if final_state:
            final_state[0].add_transition('ε', nfa.start_state)
        nfa.start_state.is_final = True
        nfas.pop(int(expression[position + 1:position + 2]))
    else:
        initial_state = State(is_final=True)
        current_state = initial_state

        nfa = NFA(initial_state)

        for element in expression_elements:
            next_state = State()
            current_state.add_transition(element, next_state)
            nfa.add_state(next_state)
            current_state = next_state

        current_state.add_transition('ε', initial_state)

    return nfa


def process_optional(exp_stack):
    expression = pop_until_open_parenthesis(exp_stack)
    expression_elements = [c for c in expression if c not in SPECIAL_CHARS]

    S1 = State()
    S2 = State(is_final=True)

    S1.add_transition('ε', S2)
    S1.add_transition(expression_elements[0], S2)

    nfa = NFA(S1)
    nfa.add_state(S2)

    return nfa


def process_character_set(expression, exp_stack):
    content = expression[1:-1]

    start_state = State()
    final_state = State(is_final=True)

    if '_' in content:
        start_char, end_char = content.split('_')
        start_state.add_range_transitions(start_char[0], end_char[0], final_state)
    else:
        for char in content:
            start_state.add_transition(char, final_state)

    nfa = NFA(start_state)
    nfa.add_state(final_state)
    return nfa


def print_nfa(nfa):
    state_index = {}
    states_to_process = [nfa.start_state]
    index = 0

    while states_to_process:
        current_state = states_to_process.pop(0)
        if current_state not in state_index:
            state_index[current_state] = index
            index += 1
            for symbol_transitions in current_state.transitions.values():
                for state in symbol_transitions:
                    if state not in state_index:
                        states_to_process.append(state)
            for state in current_state.episilon_transitions:
                if state not in state_index:
                    states_to_process.append(state)

    print("NFA:")
    for state in state_index:
        state_idx = state_index[state]
        print(f'Transições do estado {state_idx}:')
        if state.is_final:
            print(f'  Este estado é FINAL')
        for symbol, transitions in state.transitions.items():
            for transition in transitions:
                transition_idx = state_index[transition]
                print(f"  Símbolo: {symbol}, Vai para: Estado {transition_idx}")
        for transition in state.episilon_transitions:
            transition_idx = state_index[transition]
            print(f"  Símbolo: ε, Vai para: Estado {transition_idx}")


def add_epsilon_transitions_between_nfas(nfas):
    combined_nfa = nfas[0]

    for i in range(len(nfas) - 1):
        current_nfa = nfas[i]
        next_nfa = nfas[i + 1]

        final_states_current = [state for state in current_nfa.states if state.is_final]
        start_state_next = next_nfa.start_state

        for final_state in final_states_current:
            if start_state_next not in final_state.episilon_transitions:
                final_state.add_transition('ε', start_state_next)
                final_state.is_final = False

        combined_nfa.merge_nfa(next_nfa)

    return combined_nfa


def generate_nfa_from_regex(regex):
    exp_splitted = list(regex)
    nfas = []
    exp_stack = []
    skip_until_index = -1

    for i, c in enumerate(exp_splitted):
        if i < skip_until_index:
            continue
        if c == '[':
            start_index = i
            while exp_splitted[i] != ']':
                i += 1
            char_set = ''.join(exp_splitted[start_index:i + 1])
            nfa = process_character_set(char_set, exp_stack)
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
            skip_until_index = i + 1
        elif c == '+':
            nfa = process_plus_operator(exp_stack, nfas)
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        elif c == '~':
            nfa = process_concatenation(exp_stack)
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        elif c == '|':
            nfa = process_union(exp_stack)
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        elif c == '*':
            nfa = process_kleene_closure(exp_stack, nfas)
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        elif c == '?':
            nfa = process_optional(exp_stack)
            exp_stack.append(f"NFA_{len(nfas)}")
            nfas.append(nfa)
        else:
            exp_stack.append(c)

    nfa_final = add_epsilon_transitions_between_nfas(nfas)

    return nfa_final


def match_nfa(nfa, text):
    current_states = set([nfa.start_state])
    next_states = set()

    def follow_epsilon_transitions(states):
        visited = set()
        stack = list(states)

        while stack:
            state = stack.pop()
            if state not in visited:
                visited.add(state)
                stack.extend(state.episilon_transitions)

        return visited

    current_states = follow_epsilon_transitions(current_states)

    for symbol in text:
        next_states = set()
        for state in current_states:
            if symbol in state.transitions:
                next_states.update(state.transitions[symbol])
        next_states = follow_epsilon_transitions(next_states)
        current_states = next_states

    return any(state.is_final for state in current_states)


def tokenize(regexes, basic_code):
    tokens = []

    word_pattern = re.compile(r'("[^"]*"|\S+)')
    for line in basic_code.splitlines():
        #words = re.findall(r'[^\s]+', line)  # Separar por espaços
        words = word_pattern.findall(line)
        for word in words:
            matched = False
            for regex, token_type in regexes.items():
                nfa = generate_nfa_from_regex(regex)
                if match_nfa(nfa, word):
                    tokens.append((word, token_type))
                    matched = True
                    break
            if not matched:
                raise ValueError(f"Token não reconhecido: {word}")
    return tokens

def preprocess_string(basic_code):
    # Separar cada linha para tratamento individual
    lines = basic_code.strip().split('\n')
    processed_lines = []

    for line in lines:
        # Ignorar comentários
        if 'REM' in line:
            continue
        
        # Substituir espaços em strings por '_'
        in_quote = False
        processed_line = ""
        quote_content = ""
        for char in line:
            if char == '"':
                if not in_quote:
                    in_quote = True
                    processed_line += '"'
                else:
                    in_quote = False
                    processed_line += quote_content.replace(" ", "_") + '"'
                    quote_content = ""
            elif in_quote:
                quote_content += char
            else:
                processed_line += char
        
        # Adicionar espaços antes e depois de operadores e delimitadores
        delimiters = ['+', '-', '*', '/', '^', '=', '<', '>', ',', '(', ')', ':']
        buffer = ""
        new_line = ""
        for char in processed_line:
            if char in delimiters:
                new_line += ' ' + buffer + ' ' + char + ' '
                buffer = ""
            else:
                buffer += char
        new_line += buffer
        
        # Normalizar espaços múltiplos para um único espaço e trim espaços extra
        processed_line = ' '.join(new_line.split())
        processed_lines.append(processed_line)

    return ' \\n '.join(processed_lines)

def main():
    regexes = {
        "[P][R][I][N][T]": "PRINT",
        "[I][N][P][U][T]": "INPUT",
        "[L][E][T]": "LET",
        "[I][F]": "IF",
        "[T][H][E][N]": "THEN",
        "[E][L][S][E]": "ELSE",
        "[F][O][R]": "FOR",
        "[T][O]": "TO",
        "[S][T][E][P]": "STEP",
        "[N][E][X][T]": "NEXT",
        "[G][O][T][O]": "GOTO",
        "[G][O][S][U][B]": "GOSUB",
        "[R][E][T][U][R][N]": "RETURN",
        "[E][N][D]": "END",
        "[R][E][M]": "REM",
        "[D][I][M]": "DIM",
        "[R][E][A][D]": "READ",
        "[D][A][T][A]": "DATA",
        "[R][E][S][T][O][R][E]": "RESTORE",
        "[O][N]": "ON",
        "[D][E][F]": "DEF",
        "[F][N]": "FN",
        "[C][A][L][L]": "CALL",
        "[P][O][K][E]": "POKE",
        "[P][E][E][K]": "PEEK",
        "[S][T][O][P]": "STOP",
        "[S][I][N]": "SIN",
        "[C][O][S]": "COS",
        "[T][A][N]": "TAN",
        "[A][T][N]": "ATN",
        "[E][X][P]": "EXP",
        "[L][O][G]": "LOG",
        "[S][Q][R]": "SQR",
        "[I][N][T]": "INT",
        "[A][B][S]": "ABS",
        "[L][E][F][T][$]": "LEFT$",
        "[R][I][G][H][T][$]": "RIGHT$",
        "[V][A][L]": "VAL",
        "[S][T][R][$]": "STR$",
        "[M][I][D][$]": "MID$",
        "[L][E][N]": "LEN",
        "[A][S][C]": "ASC",
        "[C][H][R][$]": "CHR$",
        "[T][I][M][E][R]": "TIMER",
        "[A][N][D]": "AND",
        "[N][O][T]": "NOT",
        "[O][R]": "OR",
        '[\][n]': "NEWLINE",
        "[A_z]([0_z])*": "IDENTIFIER",
        "[A_z]([0_z])*([$])*": "STRING IDENTIFIER",
        "[+-*/^]": "ARITHMETIC_OPERATOR",
        "[=<>]": "RELATIONAL_OPERATOR",
        "[<][=]": "LESS_EQUAL_OPERATOR",
        "[>][=]": "GREATER_EQUAL_OPERATOR",
        "[<][>]": "DIFFERENT_OPERATOR",
        "[(),>:;]": "DELIMITER",
        "([0_9])+([.])*([0_9])*": "NUMBER",
        #'["]([0-z])*([ ,])*([0-z])*["]': "STRING"
        '["]([ _~])*["]': "STRING"
    }

    basic_code = """
10 REM Cálculo de fatorial usando recursão
20 INPUT "Digite um número: ", N
30 PRINT "O fatorial de "; N; " é "; FACT(N)
40 END
50 DEF FNFACT(N)
60 IF N = 0 THEN RETURN 1
70 RETURN N * FNFACT(N - 1)
    """

    # remove os acentos antes de jogar na funcao preprocess_string
    preprocessed_code = preprocess_string(''.join(ch for ch in unicodedata.normalize('NFKD', basic_code) if not unicodedata.combining(ch)))
    print(f"código preprocessado: {preprocessed_code}")
    tokens = tokenize(regexes, preprocessed_code)
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
