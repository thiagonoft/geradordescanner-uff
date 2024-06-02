import json

with open('production_rules_dict.json') as json_file:
    PRODUCTION_RULES_DICT = json.load(json_file)

ALL_NON_TERMINALS = {}
with open('production_rules.txt') as file:
    for line in file:
        non_terminal = line[0]
        non_terminal_conv = PRODUCTION_RULES_DICT[non_terminal]
        ALL_NON_TERMINALS[non_terminal_conv] = True        

with open('first.json') as json_file:
    FIRST = json.load(json_file)

PARSING_TABLE = {}
TERMINALS_SUBSET = set()
for non_terminal in FIRST:
    assert(non_terminal not in PARSING_TABLE)
    PARSING_TABLE[non_terminal] = {}

    # print("NON_TERMINALS: ", non_terminal)

    for terminal in FIRST[non_terminal]:
        TERMINALS_SUBSET.add(terminal)

for non_terminal in PARSING_TABLE:
    PARSING_TABLE[non_terminal] = {t: [] for t in TERMINALS_SUBSET}

# print("terminals:", terminals)
# print("               ", *TERMINALS_SUBSET)
# for p in PARSING_TABLE:
#     print(p)

# input()




with open('production_rules.txt') as file:
    for line in file:
        line_s = line.split("/")
        # print(line_s)
        # input()
        
        non_terminal = line_s[0][0]
        line_s[0] = line_s[0][3:] ## CORTANDO OS 3 PRIMEIROS CHARS PARA TIRAR 'A->'
        line_s[-1] = line_s[-1][:len(line_s[-1]) - 1] # TIRA O '\n' no final
        
        for rule in line_s:
            # print("rule:", rule)
            # input()

            non_terminal_conv = PRODUCTION_RULES_DICT[non_terminal]
            
            full_production = f"{non_terminal_conv} -> {' '. join([r for r in [PRODUCTION_RULES_DICT[s] for s in rule]])}"

            first_symbol_conv = PRODUCTION_RULES_DICT[rule[0]]
            first_symbol_is_non_terminal = first_symbol_conv in ALL_NON_TERMINALS
            if first_symbol_is_non_terminal:
                # pass
                # print("non_terminal (row):", non_terminal_conv)
                for t in FIRST[first_symbol_conv]:
                    # print("t (col):", t)
                    # print("P[row][col] (before):", PARSING_TABLE[non_terminal_conv][t])
                    PARSING_TABLE[non_terminal_conv][t].append(full_production)
                    # print("P[row][col] (after):", PARSING_TABLE[non_terminal_conv][t])
                #     print("---------------")
                # print("-----------------------------------------------------")
            else:
                # pass
                # print("non_terminal (row):", non_terminal_conv)
                # print("first_symbol_conv (col):", first_symbol_conv)
                # print("P[row][col] (before):", PARSING_TABLE[non_terminal_conv][first_symbol_conv])
                PARSING_TABLE[non_terminal_conv][first_symbol_conv].append(full_production)
                # print("P[row][col] (after):", PARSING_TABLE[non_terminal_conv][first_symbol_conv])
                # print("-----------------------------------------------------")

out_file = open("parsing_table.json", "w") 
json.dump(PARSING_TABLE, out_file, indent = 4) 
out_file.close()