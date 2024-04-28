import re

PROGRAM_INPUT = "int x = 10;"

KEYWORDS = [
    "int",
    "char"
]

DELIMITERS = [
    ";"
]

OPERATORS = [
    "="
]

IDENTIFIER_REGEX = r"([A-z](?:[A-z]|[0-9])*)"
# IDENTIFIER_REGEX = r"([A-z]+)|[A-z](([A-z]|[0-9])*)"

CONSTANT_REGEX = r"[0-9]+"
# ????? nao sei pq n deu
if __name__ == "__main__":
    match = re.findall(IDENTIFIER_REGEX, PROGRAM_INPUT)
    print(match)