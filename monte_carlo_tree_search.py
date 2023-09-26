import math


class Node:
    def __init__(self, name):
        self.name = name
        self.N = 0
        self.Q = 0
        self.children = []


# Initialise the tree structure based on the given problem
S0 = Node("S0")
S11 = Node("S11")
S12 = Node("S12")
S21 = Node("S21")
S22 = Node("S22")
S23 = Node("S23")

S0.children = [S11, S12]
S11.children = [S21, S22]
S12.children = [S23]

# Assign initial rewards and visit counts
S11.Q = 5 * (1 / 100)
S11.N = 5
S12.Q = 0.3
S12.N = 1
S21.Q = 2 * (1 % 5 / 10)
S21.N = 2
S22.Q = 0.4
S22.N = 3
S23.Q = 0.6
S23.N = 1


def UCT_search(s0):
    root = S0
    for _ in range(3):
        vl = tree_policy(root)
        delta = default_policy(vl.name)
        backup(vl, delta)


def tree_policy(v):
    while v.children:
        if not all(child.N > 0 for child in v.children):
            return expand(v)
        else:
            v = best_child(v, 0.9)
    return v


def expand(v):
    for child in v.children:
        if child.N == 0:
            return child
    return None


def best_child(v, c):
    best_value = -math.inf
    best_child_node = None
    for child in v.children:
        if v.N > 0 and child.N > 0:
            value = child.Q / child.N + c * math.sqrt(2 * math.log(v.N) / child.N)
        else:
            value = child.Q / child.N
        if value > best_value:
            best_value = value
            best_child_node = child
    return best_child_node


def default_policy(s):
    # Implement the default policy function based on the problem
    return 0


def backup(v, delta):
    while v is not None:
        v.N += 1
        v.Q += delta
        v = get_parent(v)


def get_parent(v):
    if v.name == "S0":
        return None
    elif v.name in ["S11", "S12"]:
        return S0
    elif v.name in ["S21", "S22"]:
        return S11
    elif v.name == "S23":
        return S12


UCT_search("S0")


# Display the tree structure with updated values after 3 iterations
def print_tree(node, indent=""):
    print(indent + f"{node.name}: N={node.N}, Q={node.Q}")
    for child in node.children:
        print_tree(child, indent + "  ")

print_tree(S0)


from graphviz import Digraph


def create_graph(node, graph=None):
    if graph is None:
        graph = Digraph()

    graph.node(node.name, f"{node.name}: N={node.N}, Q={node.Q:.2f}")

    for child in node.children:
        graph.edge(node.name, child.name)
        create_graph(child, graph)

    return graph


graph = create_graph(S0)
graph.view()
