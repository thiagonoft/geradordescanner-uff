class Tree:
    def __init__(self, data):
        self.children = None
        self.data = data

def isNonTerminal(element_str):
    return element_str[0] == '<'

def countNonTerminals(list):
    count = 0
    for element in list:
        if isNonTerminal(str(element)):
            count += 1
    return count

syntax_tree_stack = [
    "<Lines>",
    [["Integer", "<Statements>", "NewLine"], False],
    "<Statements>",
    [["<Statement>"], False],
    "<Statement>",
    [["IF", "<Expression>", "THEN", "<Statement>"], False],
    "<Expression>",
    [["<AndExp>"], False],
    "<AndExp>",
    [["<NotExp>"], False],
    "<NotExp>",
    [["<CompareExp>"], False],
    "<CompareExp>",
    [["<AddExp>", "=", "<CompareExp>"], False],
    "<AddExp>",
    [["<MultExp>"], False],
    "<MultExp>",
    [["<NegateExp>"], False],
    "<NegateExp>",
    [["<PowerExp>"], False],
    "<PowerExp>",
    [["<Value>"], False],
    "<Value>",
    ["ID"],
    "<CompareExp>",
    [["<AddExp>"], False],
    "<AddExp>",
    [["<MultExp>"], False],
    "<MultExp>",
    [["<NegateExp>"], False],
    "<NegateExp>",
    [["<PowerExp>"], False],
    "<PowerExp>",
    [["<Value>"], False],
    "<Value>",
    [["<Constant>"], False],
    "<Constant>",
    ["Integer"],
    "<Statement>",
    ["RETURN"],
]


index = 0
syntax_tree_stack.reverse()


pending_nodes = []
while True:
    child = syntax_tree_stack[index]
    parent = syntax_tree_stack[index + 1]
    
    print("child", child)
    print("parent", parent)

    n = 0
    if type(child[0]) is not list:
        n = countNonTerminals(child)
    else:
        n = countNonTerminals(child[0])
    
    print("n", n)
    if n == 0:
        child_node = Tree(child.copy())
        parent_node = Tree(parent)
        parent_node.children = child_node
        pending_nodes.append(parent_node)
    elif n == 1:
        # syntax_tree_stack[index][1] = True
        child_node = pending_nodes.pop()
        parent_node = Tree(parent)
        parent_node.children = child_node
        pending_nodes.append(parent_node)
    elif n == 2:
        parent_node = Tree(parent)
        parent_node.children = []
        for c in child[0]:
            if isNonTerminal(c):
                child_node = pending_nodes.pop()
                parent_node.children.append(child_node)
            else:
                parent_node.children.append(c)
        pass
        pass

    # if len(child[0]) > 0:
    #     node = Tree(child[0].copy())
    #     parent = Tree(parent)
    #     parent.children = node
    #     pending_nodes.append(parent)
    # else:
    #     print("LEN = 0!!!")

    index += 2
    if index == len(syntax_tree_stack):
        break

pass
"""
if len(child) == 1:

"""