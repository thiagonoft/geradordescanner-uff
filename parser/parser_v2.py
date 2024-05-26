import json
import copy
import re
import build_syntax_tree_v2
# import resource

class DecisionPoint:
  def __init__(self,
        curr_stack: list,
        curr_tokens: list,
        # curr_pt_bools: dict,
        marked_line: str,
        marked_col: str,
        numOfRulesToApply: int,
        DEBUG_RULE_TO_APPLY):
    self.curr_stack = curr_stack.copy()
    self.curr_tokens = curr_tokens.copy()
    self.marked_line = marked_line
    self.marked_col = marked_col
    self.already_tried = [False]*numOfRulesToApply
    self.DEBUG_RULE_TO_APPLY = DEBUG_RULE_TO_APPLY
    
    # mudar pra 'already_tried'
    # self.curr_pt_bools = copy.deepcopy(curr_pt_bools)
    
    # flag = False
    # for i, isMarked in enumerate(self.curr_pt_bools[line][col]):
    #     if not isMarked:
    #         self.curr_pt_bools[line][col][i] = True
    #         flag = True
    #         break
    # if not flag:
    #     raise Exception("TODOS MARCADOS!!!")
    #TODO: desmarcar qnd for outra regra


def isNonTerminal(element_str):
    pattern = "<(.+)>"
    return True if re.match(pattern, element_str) else False
    # return element_str[0] == '<'

def convertToken(curr_token_annotated):
    token_without_annotation = curr_token_annotated[1] # second element of the token
    if token_without_annotation in TYPE_MAPPING_DICT:
        return TYPE_MAPPING_DICT[token_without_annotation]
    else:
        return token_without_annotation

def initParsingTableCopyWithBooleans(pt):
    result_pt = {}
    for line in pt:
        for col in pt[line]:
            n = len(pt[line][col])
            if n > 1:
                if not line in result_pt:
                    result_pt[line] = {}
                result_pt[line][col] = [False]*n
    
    return result_pt

def decideIndexOfRuleToApply(line, col):
    if len(decision_points) == 0:
        return len(PARSING_TABLE[line][col]) - 1
    
    lp = decision_points[-1]
    if JUST_BACKTRACKED:
        if DEBUG_IS_INDEX_REVERSED:
            i = getLastFalseIndex(lp.already_tried)
            return i
        else:
            return len(PARSING_TABLE[line][col]) - 1
    else:
        return len(PARSING_TABLE[line][col]) - 1
    # raise Exception("Todas as regras possiveis foram marcadas!!")

with open('parsing_table.json') as json_file:
    PARSING_TABLE = json.load(json_file)

def markDecisionPoint(dp: DecisionPoint):
    marked = False
    if DEBUG_IS_INDEX_REVERSED:
        for i, isMarked in enumerate(reversed(dp.already_tried)):
            if not isMarked:
                dp.already_tried[len(dp.already_tried) - i - 1] = True
                marked = True
                break
    else:
        for i, isMarked in enumerate(dp.already_tried):
            if not isMarked:
                dp.already_tried[i] = True
                marked = True
                break
    return marked 
    # if not marked:
    #     raise Exception("Falha ao marcar DecisionPoint!! Todas as possibilidades foram marcadas!!")

def backtrack():
    global decision_points
    if len(decision_points) == 0:
        raise Exception(f"Não há pontos para fazer backtracking. Erro de sintaxe no token {curr_token_annotated}. A entrada é inválida.")
    last_point: DecisionPoint = decision_points[-1]
    print(f"Backtracking on decision {last_point.DEBUG_RULE_TO_APPLY}...")
    marked = markDecisionPoint(last_point)
    #TODO: tratar qnd tiver 0 possibilidades (regra nao é mais vivel)
    c = last_point.already_tried.count(False)
    if marked and c == 0:
        decision_points.pop()
        last_point = decision_points[-1]
        print("POP!")
        backtrack()
        return
    
    l = last_point.marked_line
    c = last_point.marked_col
    prev = PARSING_TABLE[l][c]
    print("Remaining possibilities:")
    for i, isMarked in enumerate(last_point.already_tried):
        if not isMarked:
            print("    ", prev[i])
    
    global stack
    stack = last_point.curr_stack
    
    global tokens
    tokens = last_point.curr_tokens

    # TODO: verificar se nao tem que mudar algo mais assim que tem backtracking
    global stack_top
    stack_top = last_point.marked_line

    global curr_token
    curr_token = last_point.marked_col

    global JUST_BACKTRACKED
    JUST_BACKTRACKED = True

    global ALLOW_JUST_BACKTRACKED
    ALLOW_JUST_BACKTRACKED = True
    
def getLastFalseIndex(l: list[bool]):
    for i, e in enumerate(reversed(l)):
        if e == False:
            return len(l) - i - 1

def justBacktracked():
    global decision_points
    if len(decision_points) == 0:
        return False
    
    lp = decision_points[-1]
    global stack
    global tokens
    return (stack == lp.curr_stack) and (tokens == lp.curr_tokens)
    

tokens = []
# with open('tokens_input.txt', "r") as file:
#     for line in file:
#         tokens.append(eval(line[:-1])) # removes \n

# FOR TESTING ONLY
test_tokens_valid = """('60', 'NUMBER')
('IF', 'IF')
('N', 'ID')
('=', 'RELATIONAL_OPERATOR')
('0', 'NUMBER')
('THEN', 'THEN')
('RETURN', 'RETURN')
('NEWLINE', 'NEWLINE')"""

test_tokens_valid_2 = """('10', 'NUMBER')
('DIM', 'DIM')
('N', 'ID')
('(', '(')
('25', 'NUMBER')
(')', ')')
('NEWLINE', 'NEWLINE')"""

test_tokens_valid_3 = """('10', 'NUMBER')
('READ', 'READ')
('A1', 'ID')
(',', ',')
('A2', 'ID')
(',', ',')
('A3', 'ID')
(',', ',')
('A4', 'ID')
('NEWLINE', 'NEWLINE')"""

test_tokens_invalid = """('IF', 'IF')
('N', 'ID')
('=', 'RELATIONAL_OPERATOR')
('0', 'NUMBER')
('THEN', 'THEN')
('RETURN', 'RETURN')
('NEWLINE', 'NEWLINE')"""

for line in test_tokens_valid_2.split("\n"):
    tokens.append(eval(line))
tokens.append("($, $)")



# TODO: tirar isso e receber direto do gerador de scanner
TYPE_MAPPING_DICT = {
    "NUMBER": "Integer",
    "RELATIONAL_OPERATOR": "=",
}

DEBUG_IS_INDEX_REVERSED = True
JUST_BACKTRACKED = False
ALLOW_JUST_BACKTRACKED = False

decision_points: list[DecisionPoint] = []
# pt_bools = initParsingTableCopyWithBooleans(PARSING_TABLE)

stack = ['$', "<Lines>"]
stack_top = stack[-1]
curr_token_annotated = tokens.pop(0)
curr_token = convertToken(curr_token_annotated)

while len(stack) > 0:
    if JUST_BACKTRACKED:
        if ALLOW_JUST_BACKTRACKED:
            ALLOW_JUST_BACKTRACKED = False
        else:
            JUST_BACKTRACKED = False
    
    if isNonTerminal(stack_top):
        if not curr_token in PARSING_TABLE[stack_top]:
            #TODO: backtrack aqui (para o caso de teste atual, a primeira regra <CompareExp> não
            # pode virar '<AddExp>' e sim tem que virar '<AddExp> = <CompareExp>'

            # acho que ta dando problema no backtracking com o curr_token e stack_top
            backtrack()
            continue
            # break
            # raise Exception("COLUNA vazia na tabela de parsing ! Erro de sintaxe!!!")
        
        rules_to_apply = PARSING_TABLE[stack_top][curr_token]
        #TODO: talvez tratar quando mesmo que na tabela de parsing tenha mais de uma entry se
        # com as restrições tiver só uma nao criar decision point
        if len(rules_to_apply) > 1:
            line = str(stack_top)
            col = str(curr_token)

            # TODO: revisar a função 'decideIndexOfRuleToApply'
            index = decideIndexOfRuleToApply(line, col)
            rule_to_apply = PARSING_TABLE[line][col][index]
            print(rule_to_apply)
            
            if not JUST_BACKTRACKED:
                new_dp = DecisionPoint(stack, tokens, line, col, len(rules_to_apply), rule_to_apply)
                decision_points.append(new_dp)
        elif len(rules_to_apply) == 1:
            rule_to_apply = rules_to_apply[0]
            print(rule_to_apply)
        else:
            backtrack()
            continue
            # raise Exception("LINHA vazia na tabela de parsing ! Erro de sintaxe!!!")
            # TODO: backtrack
        
        right_hand_side = rule_to_apply.split()[2:]
        
        stack.pop()
        for s in reversed(right_hand_side):
            stack.append(s)
        stack_top = stack[-1]
    else:
        if stack_top == '$':
            if len(tokens) > 0:
                backtrack()
                continue
            else:
                print("OK! Entrada aceita.")
                break
        stack.pop()
        stack_top = stack[-1]

        if len(tokens) == 0:
            backtrack()
            continue
        curr_token_annotated = tokens.pop(0)
        curr_token = convertToken(curr_token_annotated)
pass

# testando memoria
# a = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(a)