import json

with open('parsing_table.json') as json_file:
    PARSING_TABLE = json.load(json_file)

tokens = []
# with open('tokens_input.txt', "r") as file:
#     for line in file:
#         tokens.append(eval(line[:-1])) # removes \n

# FOR TESTING ONLY
one_line_token = """('60', 'NUMBER')
('IF', 'IF')
('N', 'IDENTIFIER')
('=', 'RELATIONAL_OPERATOR')
('0', 'NUMBER')
('THEN', 'THEN')
('RETURN', 'RETURN')
('1', 'NUMBER')"""
for line in one_line_token.split("\n"):
    tokens.append(eval(line))





MAPPING_DICT = {
    "NUMBER": "Integer"
}

stack = ['$', "<Lines>"]

symbol = stack.pop()
token = tokens.pop(0)[1] # second element of the first token
token_type_conv = MAPPING_DICT[token] 
look_ahead = PARSING_TABLE[symbol][token_type_conv]
look_ahead = look_ahead[1] # adhoc decision

symbols_to_stack = look_ahead.split(" ")[2:]

print(symbols_to_stack)

while(len(symbols_to_stack) > 0):
    stack.append(symbols_to_stack.pop(0))

print(stack)