import json

# Opening JSON file
with open('symbols_dict.json') as json_file:
    symbols_conversion = json.load(json_file)

if __name__ == "__main__":
    FIRST =  {'E': {'S', 'R', 'F', 'j', 'k', 'i', 'X', 'h', 'Q', 'L', 'I', 'Y', 'm', 'M', 'n', 'l', 'G', 'e', 'c', 'g', 'U', 'W'}, 'w': {'%', '[', '`', 'J', 'A', '*'}, 'K': {'A'}, 'r': {'%', 'v', '[', '`', 'J', 'A', '*'}, 'D': {'A'}, 'a': {'U', 'o'}, 'd': {'%', '`', 'J', 'A', '*'}, '#': {'}'}, 'B': {'S', 'R', 'F', 'U', 'j', 'k', 'i', 'X', 'h', 'Q', 'L', 'Y', 'm', 'M', 'n', 'l', 'G', 'e', 'c', 'g', 'I', 'W'}, 'H': {'%', 'A', '`'}, 'f': {'%', '`', 'A', '~', '*', 'v', '[', 'J'}, 'q': {'%', 'v', '[', '`', 'J', 'A', '*'}, 'z': {'%', '[', '`', 'J', 'A', '*'}, 't': {'%', 'v', '[', '`', 'J', 'A', '*'}, '!': {'%', '`', 'J', 'A', '*'}, 'p': {'%', 'A', '`'}, 'V': {'J'}, 'y': {'%', '[', '`', 'J', 'A', '*'}, 'Z': {'%', '`', 'J', 'A', '*'}, 'x': {'%', '[', '`', 'J', 'A', '*'}, 'N': {'%', 'v', '[', '`', 'J', 'A', '*'}}
    for key in FIRST:
        print(f"FIRST({symbols_conversion[key]}) = {[symbols_conversion[f] for f in FIRST[key]]}")