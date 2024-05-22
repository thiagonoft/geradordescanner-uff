import json

def isNonTerminal(element_str):
    return element_str[0] == '<'

def convertToken(curr_token_annotated):
    token_without_annotation = curr_token_annotated[1] # second element of the token
    if token_without_annotation in TYPE_MAPPING_DICT:
        return TYPE_MAPPING_DICT[token_without_annotation]
    else:
        return token_without_annotation

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
            rule_to_apply = ADHOC_DECISION_MAPPING_DICT[line + col]
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