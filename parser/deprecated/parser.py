import json
import build_syntax_tree_v2

class Tree:
    def __init__(self, data):
        self.children = None
        self.data = data

def isNonTerminal(element_str):
    return element_str[0] == '<'

# def countNonTerminals(list):
#     count = 0
#     for element in list:
#         if str(element)[0] == '<':
#             count += 1
#     return count

with open('parsing_table.json') as json_file:
    PARSING_TABLE = json.load(json_file)

tokens = []
# with open('tokens_input.txt', "r") as file:
#     for line in file:
#         tokens.append(eval(line[:-1])) # removes \n

# FOR TESTING ONLY
one_line_token = """('60', 'NUMBER')
('IF', 'IF')
('N', 'ID')
('=', 'RELATIONAL_OPERATOR')
('0', 'NUMBER')
('THEN', 'THEN')
('RETURN', 'RETURN')"""
for line in one_line_token.split("\n"):
    tokens.append(eval(line))
tokens.append("$")




TYPE_MAPPING_DICT = {
    "NUMBER": "Integer",
    "RELATIONAL_OPERATOR": "=",
}

ADHOC_DECISION_MAPPING_DICT = {
    "<Lines>Integer":"<Lines> -> Integer <Statements> NewLine",
    "<Statements>IF":"<Statements> -> <Statement>",
    "<Expression>ID":"<Expression> -> <AndExp>",
    "<AndExp>ID":"<AndExp> -> <NotExp>",
    "<CompareExp>ID":"<CompareExp> -> <AddExp> = <CompareExp>",
    "<AddExp>ID":"<AddExp> -> <MultExp>",
    "<MultExp>ID":"<MultExp> -> <NegateExp>",
    "<PowerExp>ID":"<PowerExp> -> <Value>",
    "<Value>ID":"<Value> -> ID",
    "<CompareExp>Integer":"<CompareExp> -> <AddExp>",
    "<AddExp>Integer":"<AddExp> -> <MultExp>",
    "<MultExp>Integer":"<MultExp> -> <NegateExp>",
    "<PowerExp>Integer":"<PowerExp> -> <Value>"
}

stack = ['$', "<Lines>"]
stack_top = stack.pop()
curr_token = tokens.pop(0)
token_without_annotation = curr_token[1] # second element of the first token
if token_without_annotation in TYPE_MAPPING_DICT:
    curr_token_type = TYPE_MAPPING_DICT[token_without_annotation]
else:
    curr_token_type = token_without_annotation

syntax_tree_stack = []
syntax_tree_stack_2 = []

flag = True
while flag:
    while stack_top == curr_token_type:
        stack_top = stack.pop()
        curr_token = tokens.pop(0)
        if curr_token == "$":
            flag = False
            break

        token_without_annotation = curr_token[1] # second element of the first token

        if token_without_annotation in TYPE_MAPPING_DICT:
            curr_token_type = TYPE_MAPPING_DICT[token_without_annotation]
        else:
            curr_token_type = token_without_annotation

    if curr_token == "$":
        break

    look_ahead = PARSING_TABLE[stack_top][curr_token_type]
    if len(look_ahead) > 1:
        line = str(stack_top)
        col = str(curr_token_type)
        look_ahead = ADHOC_DECISION_MAPPING_DICT[line + col]
    else:
        look_ahead = look_ahead[0]

    
    symbols_to_stack = look_ahead.split(" ")[2:]
    # print(look_ahead)

    parent_node = Tree(look_ahead.split(" ")[0])
    child_nodes = symbols_to_stack.copy()
    parent_node.children = child_nodes
            

    syntax_tree_stack.append(parent_node)

    # syntax_tree_stack.append(stack_top)
    # print(look_ahead)
    # if countNonTerminals(symbols_to_stack) > 0:
    #     syntax_tree_stack.append((symbols_to_stack.copy(), False))
    # else:
    #     syntax_tree_stack.append(symbols_to_stack.copy())

    while(len(symbols_to_stack) > 0):
        popped = symbols_to_stack.pop()
        stack.append(popped)
        # print("popped", popped)

    stack_top = stack.pop()
    pass

pass
# print(syntax_tree_stack)
o = build_syntax_tree_v2.build_syntax_tree(syntax_tree_stack)
print(o)
# stack_top = stack.pop()
# while stack_top == curr_token_type:
#     curr_token = tokens.pop(0)
#     token_without_annotation = curr_token[1] # second element of the first token
#     if token_without_annotation in TYPE_MAPPING_DICT:
#         curr_token_type = TYPE_MAPPING_DICT[token_without_annotation]
#     else:
#         curr_token_type = token_without_annotation



# print(tokens)
# print(stack)
# print("--------------------")