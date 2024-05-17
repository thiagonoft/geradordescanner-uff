import json

with open('first.json') as json_file:
    FIRST = json.load(json_file)

with open('parsing_table.json') as json_file:
    PARSING_TABLE = json.load(json_file)
