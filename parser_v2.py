import json
import re

class DecisionPoint:
  def __init__(self,
        curr_stack: list,
        curr_tokens: list,
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

class Tree():
    def __init__(self, data, children = None):
        self.children = children
        self.data = data

def computeNode(node: Tree, lines: list[str]):
    line = lines.pop(0)
    lhs = line.split()[0]
    rhs = line.split()[2:]
    
    node.data = lhs
    node.children = []
    for c in rhs:
        if isNonTerminal(c):
            node.children.append(computeNode(Tree(c), lines))
        else:
            node.children.append(c)
    return node

def printTree(root: Tree, level=0):
    print("--" * level, root.data)
    for child in root.children:
        if type(child) is Tree:
            printTree(child, level + 1)
        else:
            print("--" * (level + 1), child)

def isNonTerminal(element_str):
    pattern = "<(.+)>"
    return True if re.match(pattern, element_str) else False

def convertToken(curr_token_annotated):
    token_without_annotation = curr_token_annotated[1] # second element of the token
    if token_without_annotation in TYPE_MAPPING_DICT:
        return TYPE_MAPPING_DICT[token_without_annotation]
    elif token_without_annotation[0] in "+-*/^=<><=>=<>(),>:;":
        return curr_token_annotated[0]
    else:
        return curr_token_annotated[1]

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

with open('parser/parsing_table.json') as json_file:
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
    # print(f"Backtracking on decision {last_point.DEBUG_RULE_TO_APPLY}...")
    marked = markDecisionPoint(last_point)
    
    c = last_point.already_tried.count(False)
    if marked and c == 0:
        decision_points.pop()
        last_point = decision_points[-1]
        # print("POP!")
        backtrack()
        return
    
    # l = last_point.marked_line
    # c = last_point.marked_col
    # prev = PARSING_TABLE[l][c]
    # print("Remaining possibilities:")
    # for i, isMarked in enumerate(last_point.already_tried):
    #     if not isMarked:
            # print("    ", prev[i])
    
    global stack
    stack = last_point.curr_stack
    
    global tokens
    tokens = last_point.curr_tokens

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

def substituteTerminals(node: Tree, tokens_to_substitute: list):
    for i, c in enumerate(node.children):
        if type(c) is Tree:
            substituteTerminals(c, tokens_to_substitute)
        else:
            tok = tokens_to_substitute.pop(0)
            node.children[i] = tok[0]

def buildSyntaxTree():
    print("-----Arvore Sintatica-----")
    new_tokens = ORIGINAL_TOKENS.copy()
    new_tokens_2 = ORIGINAL_TOKENS.copy()
    new_stack = ['$', "<Lines>"]
    new_stack_top = new_stack[-1]
    new_curr_token_annotated = new_tokens.pop(0)
    new_curr_token = convertToken(new_curr_token_annotated)
    syntax_tree_stack = []

    while len(new_stack) > 0:
        if isNonTerminal(new_stack_top):
            rules_to_apply = PARSING_TABLE[new_stack_top][new_curr_token]
            if len(rules_to_apply) > 1:
                consumedDecisionPoint = decision_points.pop(0) # talvez seja bom fzr copia
                
                dp_line = consumedDecisionPoint.marked_line
                dp_col = consumedDecisionPoint.marked_col
                dp_index = getLastFalseIndex(consumedDecisionPoint.already_tried)
                rule_to_apply = PARSING_TABLE[dp_line][dp_col][dp_index]
                # print(rule_to_apply)
                # syntax_tree_stack.append(rule_to_apply)
                # print(f"new_curr_token_annotated {new_curr_token_annotated} new_stack_top {new_stack_top}")
                # syntax_element = f"{new_curr_token_annotated[0]}"
                syntax_tree_stack.append(rule_to_apply)
            elif len(rules_to_apply) == 1:
                rule_to_apply = rules_to_apply[0]
                # print(rule_to_apply)
                # syntax_tree_stack.append(rule_to_apply)
                # print(f"new_curr_token_annotated {new_curr_token_annotated} new_stack_top {new_stack_top}")
                syntax_tree_stack.append(rule_to_apply)
            else:
                # backtrack()
                # continue
                # raise Exception("LINHA vazia na tabela de parsing ! Erro de sintaxe!!!")
                raise Exception("???")
            
            right_hand_side = rule_to_apply.split()[2:]
            
            new_stack.pop()
            for s in reversed(right_hand_side):
                new_stack.append(s)
            new_stack_top = new_stack[-1]
        else:
            if new_stack_top == '$':
                if len(new_tokens) > 0:
                    # backtrack()
                    raise Exception("???")
                    # continue
                else:
                    # print("OK! Entrada aceita.")
                    break
            new_stack.pop()
            new_stack_top = new_stack[-1]

            if len(new_tokens) == 0:
                # backtrack()
                raise Exception("???")
                # continue
            # print(f"new_curr_token_annotated {new_curr_token_annotated} new_stack_top {new_stack_top}")
            new_curr_token_annotated = new_tokens.pop(0)
            new_curr_token = convertToken(new_curr_token_annotated)
    node = computeNode(Tree(""), syntax_tree_stack)
    substituteTerminals(node, new_tokens_2)
    printTree(node)


tokens = []
with open('tests/testDefault_parser.in', "r") as file:
    for line in file:
        tokens.append(eval(line[:-1])) # removes \n

# test_tokens_valid_3 = """('10', 'NUMBER')
# ('READ', 'READ')
# ('A1', 'ID')
# (',', ',')
# ('A2', 'ID')
# (',', ',')
# ('A3', 'ID')
# (',', ',')
# ('A4', 'ID')
# ('NEWLINE', 'NEWLINE')
# ('20', 'NUMBER')
# ('READ', 'READ')
# ('A5', 'ID')
# (',', ',')
# ('A6', 'ID')
# (',', ',')
# ('A7', 'ID')
# (',', ',')
# ('A8', 'ID')
# ('NEWLINE', 'NEWLINE')"""

# test_tokens_invalid = """('IF', 'IF')
# ('N', 'ID')
# ('=', 'RELATIONAL_OPERATOR')
# ('0', 'NUMBER')
# ('THEN', 'THEN')
# ('RETURN', 'RETURN')
# ('NEWLINE', 'NEWLINE')"""


# for line in test_tokens_valid_3.split("\n"):
#     tokens.append(eval(line))
tokens.append("($, $)")
ORIGINAL_TOKENS = tokens.copy()

# TODO: tirar isso e receber direto do gerador de scanner
TYPE_MAPPING_DICT = {
    "NUMBER": "Integer",
    "IDENTIFIER":"ID",
}

DEBUG_IS_INDEX_REVERSED = True
JUST_BACKTRACKED = False
ALLOW_JUST_BACKTRACKED = False

decision_points: list[DecisionPoint] = []

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
            backtrack()
            continue
            # break
            # raise Exception("COLUNA vazia na tabela de parsing ! Erro de sintaxe!!!")
        
        rules_to_apply = PARSING_TABLE[stack_top][curr_token]
        if len(rules_to_apply) > 1:
            line = str(stack_top)
            col = str(curr_token)

            index = decideIndexOfRuleToApply(line, col)
            rule_to_apply = PARSING_TABLE[line][col][index]
            # print(rule_to_apply)
            
            if not JUST_BACKTRACKED:
                new_dp = DecisionPoint(stack, tokens, line, col, len(rules_to_apply), rule_to_apply)
                decision_points.append(new_dp)
        elif len(rules_to_apply) == 1:
            rule_to_apply = rules_to_apply[0]
            # print(rule_to_apply)
        else:
            backtrack()
            continue
            # raise Exception("LINHA vazia na tabela de parsing ! Erro de sintaxe!!!")
        
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

buildSyntaxTree()
pass
# testando memoria
# a = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(a)