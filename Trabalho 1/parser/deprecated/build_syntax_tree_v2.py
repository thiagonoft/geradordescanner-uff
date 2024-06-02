class Tree:
    def __init__(self, data):
        self.children = None
        self.data = data

def isNonTerminal(element_str):
    return element_str[0] == '<'

def build_syntax_tree(syntax_tree_stack: list, root=None):
    root = syntax_tree_stack.pop(0)
    output = []
    for i, c in enumerate(root.children):
        if isNonTerminal(c):
            output.append(build_syntax_tree(syntax_tree_stack, root))
        else:
            output.append(c)
    return output