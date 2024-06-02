import re
class Tree():
    def __init__(self, data, children = None):
        self.children = children
        self.data = data

def isNonTerminal(element_str):
    pattern = "<(.+)>"
    return True if re.match(pattern, element_str) else False

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

if __name__ == "__main__":
    entrada = """<Lines> -> Integer <Statements> NewLine
    <Statements> -> <Statement>
    <Statement> -> READ <IDList>
    <IDList> -> ID
    """
    
    entrada2 = """<Lines> -> Integer <Statements> NewLine <Lines>
    <Statements> -> <Statement>
    <Statement> -> READ <IDList>
    <IDList> -> ID , <IDList>
    <IDList> -> ID , <IDList>
    <IDList> -> ID , <IDList>
    <IDList> -> ID
    <Lines> -> Integer <Statements> NewLine
    <Statements> -> <Statement>
    <Statement> -> READ <IDList>
    <IDList> -> ID , <IDList>
    <IDList> -> ID , <IDList>
    <IDList> -> ID , <IDList>
    <IDList> -> ID"""

    # line = entrada.split("\n")[0]
    # lhs = line.split()[0]
    # rhs = line.split()[2:]

    lines = entrada2.split("\n")
    node = computeNode(Tree(""), lines)
    printTree(node)
            
    # for line in entrada.split("\n"):
    #     lhs = line.split()[0]
    #     rhs = line.split()[2:]

    #     node = 


