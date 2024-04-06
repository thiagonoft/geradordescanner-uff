# *(.(+(a,b),+(a,E)))
 
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