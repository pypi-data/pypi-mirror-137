import ast
import networkx as nx

ASSIGN = 'Assign'
WHILE = 'While'
RETURN = 'Return'
CONSTANT = 'Constant'
NAME = 'Name'
COMPARE = 'Compare'
AUG_ASSIGN = 'AugAssign'

index = 1

G = nx.DiGraph()


def get_node_type(elem):
    return elem.__class__.__name__


def get_node_text(str1, str2=""):
    global index
    tmp = str(index) + ". " + str1 + '\n' + str2
    index += 1
    return tmp


def add_root(elem):
    type_name = get_node_type(elem)
    root_name = elem.name
    root = get_node_text(type_name, root_name)
    G.add_node(root, color='green')
    return root


def add_name(elem, parent):
    val_name = elem.id
    name_node = get_node_text(NAME, val_name)
    G.add_node(name_node, color='blue')
    G.add_edge(parent, name_node)


def add_constant(elem, parent):
    value = elem.value.value
    value_node = get_node_text(CONSTANT, str(value))
    G.add_node(value_node, color='yellow')
    G.add_edge(parent, value_node)


def add_assign(elem, parent):
    assign_node = get_node_text(ASSIGN)
    G.add_node(assign_node, color='red')
    G.add_edge(parent, assign_node)

    add_name(elem.targets[0], assign_node)

    right_name = get_node_type(elem.value)
    if right_name == NAME:
        add_name(elem.value, assign_node)
    else:
        add_constant(elem, assign_node)


def add_while(elem, parent):
    while_node = get_node_text(WHILE)
    G.add_node(while_node, color='orange')
    G.add_edge(parent, while_node)

    add_compare(elem.test, while_node)
    body_node = get_node_text("Body")
    G.add_node(body_node)
    G.add_edge(while_node, body_node)
    build_graph(elem, body_node)


def add_return(elem, parent):
    return_node = get_node_text(RETURN)
    G.add_node(return_node, color='pink')
    G.add_edge(parent, return_node)
    add_name(elem.value, return_node)


def add_compare(elem, parent):
    compare_node = get_node_text(COMPARE, '<')
    G.add_node(compare_node, color='purple')
    G.add_edge(parent, compare_node)

    add_name(elem.left, compare_node)
    add_name(elem.comparators[0], compare_node)


def add_aug_assign(elem, pred):
    aug_assign_node = get_node_text(AUG_ASSIGN, get_node_type(elem.op))
    G.add_node(aug_assign_node, color='brown')
    G.add_edge(pred, aug_assign_node)

    add_name(elem.target, aug_assign_node)

    one_node = get_node_text(CONSTANT, '1')
    G.add_node(one_node, color='yellow')
    G.add_edge(aug_assign_node, one_node)


def build_graph(tree, pred):
    for elem in tree.body:
        if get_node_type(elem) == ASSIGN:
            add_assign(elem, pred)
        elif get_node_type(elem) == WHILE:
            add_while(elem, pred)
        elif get_node_type(elem) == RETURN:
            add_return(elem, pred)
        else:
            add_aug_assign(elem, pred)


def plot_ast():
    ast_tree = get_ast().body[0]
    pred = add_root(ast_tree)
    build_graph(ast_tree, pred)

    p = nx.drawing.nx_pydot.to_pydot(G)
    p.write_png('artifacts/example.png')


def fib(n: int):
    curr = 0
    next = 1
    ind = 0
    while ind < n:
        tmp = next
        next += curr
        curr = tmp
        ind += 1
    return curr


def get_ast_string():
    return ast.dump(get_ast(), indent=4)


def get_ast():
    return ast.parse("""def fib(n: int):
    curr = 0
    next = 1
    ind = 0
    while ind < n:
        tmp = next
        next += curr
        curr = tmp
        ind += 1
    return curr""")


if __name__ == '__main__':
    plot_ast()