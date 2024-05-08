symbols_conversion = {
    "D":"<Lines>",
    "B":"<Statements>",
    "E":"<Statement>",
    "a":"<Access>",
    "V":"<ID List>",
    "d":"<Value List>",
    "H":"<Constant List>",
    "K":"<Integer List>",
    "q":"<Expression List>",
    "f":"<Print List>",
    "N":"<Expression>",
    "r":"<And Exp>",
    "t":"<Not Exp>",
    "w":"<Compare Exp>",
    "x":"<Add Exp>",
    "y":"<Mult Exp>",
    "z":"<Negate Exp>",
    "!":"<Power Exp>",
    "#":"<Power Exp'>",
    "Z":"<Value>",
    "p":"<Constant>",
    "A":"Integer",
    "C":"NewLine",
    "¨":"':'",
    "F":"CLOSE",
    "&":"'#'",
    "G":"DATA",
    "I":"DIM",
    "J":"ID",
    "*":"'('",
    "(":"')'",
    "L":"END",
    "M":"FOR",
    ")":"'='",
    "O":"TO",
    "P":"STEP",
    "Q":"GOTO",
    "R":"GOSUB",
    "S":"IF",
    "T":"THEN",
    "U":"INPUT",
    "<":"','",
    "W":"LET",
    "X":"NEXT",
    "Y":"OPEN",
    "b":"AS",
    "c":"POKE",
    "e":"PRINT",
    "g":"READ",
    "h":"RETURN",
    "i":"RESTORE",
    "j":"RUN",
    "k":"STOP",
    "l":"SYS",
    "m":"WAIT",
    "n":"Remark",
    "o":"OUTPUT",
    "$":"Real",
    "s":"OR"
}

if __name__ == "__main__":
    production_rules = ""
    with open("production_rules.txt", "r") as f:
        for line in f:
            production_rules += line
    # print(production_rules)

    p = list(production_rules)
    for i, c in enumerate(p):
        if c in symbols_conversion:
            p[i] = '_'
        # if c in symbols_conversion:
        #     p[i] = symbols_conversion[c]
        
    print("".join(p))