import json
import copy
# import resource

class DecisionPoint:
  def __init__(self,
        curr_stack: list,
        curr_tokens: list,
        # curr_pt_bools: dict,
        marked_line: str,
        marked_col: str):
    self.curr_stack = curr_stack.copy()
    self.curr_tokens = curr_tokens.copy()
    self.marked_line = marked_line
    self.marked_col = marked_col
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
    return element_str[0] == '<'

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

# def decideIndexOfRuleToApply(line, col, pt_bools):
#     for i, isMarked in enumerate(pt_bools[line][col]):
#         if not isMarked:
#             return i
#     raise Exception("Todas as regras possiveis foram marcadas!!")

# SÓ PRA TESTE
def decideIndexOfRuleToApply(line, col, pt_bools):
    for i, isMarked in enumerate(pt_bools[line][col]):
        if not isMarked:
            return len(pt_bools[line][col]) - i - 1
    raise Exception("Todas as regras possiveis foram marcadas!!")

with open('parsing_table.json') as json_file:
    PARSING_TABLE = json.load(json_file)

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

test_tokens_invalid = """('IF', 'IF')
('N', 'ID')
('=', 'RELATIONAL_OPERATOR')
('0', 'NUMBER')
('THEN', 'THEN')
('RETURN', 'RETURN')
('NEWLINE', 'NEWLINE')"""

for line in test_tokens_invalid.split("\n"):
    tokens.append(eval(line))
tokens.append("($, $)")




TYPE_MAPPING_DICT = {
    "NUMBER": "Integer",
    "RELATIONAL_OPERATOR": "=",
}

# ADHOC_DECISION_MAPPING_DICT = {
#     "<Lines>Integer":"<Lines> -> Integer <Statements> NewLine",
#     "<Statements>IF":"<Statements> -> <Statement>",
#     "<Expression>ID":"<Expression> -> <AndExp>",
#     "<AndExp>ID":"<AndExp> -> <NotExp>",
#     "<CompareExp>ID":"<CompareExp> -> <AddExp> = <CompareExp>",
#     "<AddExp>ID":"<AddExp> -> <MultExp>",
#     "<MultExp>ID":"<MultExp> -> <NegateExp>",
#     "<PowerExp>ID":"<PowerExp> -> <Value>",
#     "<Value>ID":"<Value> -> ID",
#     "<CompareExp>Integer":"<CompareExp> -> <AddExp>",
#     "<AddExp>Integer":"<AddExp> -> <MultExp>",
#     "<MultExp>Integer":"<MultExp> -> <NegateExp>",
#     "<PowerExp>Integer":"<PowerExp> -> <Value>"
# }

decision_points = []
pt_bools = initParsingTableCopyWithBooleans(PARSING_TABLE)

stack = ['$', "<Lines>"]
stack_top = stack[-1]
curr_token_annotated = tokens.pop(0)
curr_token = convertToken(curr_token_annotated)

while len(stack) > 0:
    if isNonTerminal(stack_top):
        rules_to_apply = PARSING_TABLE[stack_top][curr_token]
        # TODO: implementar back-tracking aqui
        if len(rules_to_apply) > 1:
            line = str(stack_top)
            col = str(curr_token)

            new_dp = DecisionPoint(stack, tokens, line, col)
            decision_points.append(new_dp)
            
            index = decideIndexOfRuleToApply(line, col, pt_bools)
            rule_to_apply = PARSING_TABLE[line][col][index]
            # rule_to_apply = ADHOC_DECISION_MAPPING_DICT[line + col]
        elif len(rules_to_apply) == 1:
            rule_to_apply = rules_to_apply[0]
        else:
            raise Exception("Erro!!!")
        
        right_hand_side = rule_to_apply.split()[2:]
        
        stack.pop()
        for s in reversed(right_hand_side):
            stack.append(s)
        stack_top = stack[-1]
    else:
        if stack_top == '$':
            break
        stack.pop()
        stack_top = stack[-1]
        curr_token_annotated = tokens.pop(0)
        curr_token = convertToken(curr_token_annotated)
pass

# testando memoria
# a = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(a)