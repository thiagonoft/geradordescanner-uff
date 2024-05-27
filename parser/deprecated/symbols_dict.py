import json

# Opening JSON file
with open('symbols_dict.json') as json_file:
    symbols_conversion = json.load(json_file)

if __name__ == "__main__":
    production_rules = ""
    with open("production_rules.txt", "r") as f:
        for line in f:
            production_rules += line
    # print(production_rules)

    p = list(production_rules)
    curr = ""
    for i, c in enumerate(p):
        if c in symbols_conversion:
            p[i] = symbols_conversion[c] + " "
            curr = p[i]
        else:
            if c in ['-', '>']:
                p[i] = '-' if c == '-' else "> "
            else:
                if c in ['/', '\n']:
                    p[i] = f"\n\t| " if c == '/' else '\n'
                else:
                    p[i] = "?????"
            
            # if c in ['-', '>']:
            #     p[i] = ' ::' if c == '-' else "= "
            # else:
            #     if c in ['/', '\n']:
            #         p[i] = "\n\t| " if c == '/' else '\n'
            #     else:
            #         p[i] = "?????"
        
        # if c in symbols_conversion:
        #     p[i] = symbols_conversion[c]
        
    print("".join(p))