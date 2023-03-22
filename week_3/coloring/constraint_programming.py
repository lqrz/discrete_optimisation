from typing import List, Tuple, Dict, Set
from operator import itemgetter
from collections import Counter
from collections import deque
from collections import defaultdict


def select_node(nodes_sorted: List[Tuple[int, int]], nodes_selected: Set[int]) -> int:
    nodes = list(filter(lambda x: x not in nodes_selected, map(itemgetter(0), nodes_sorted)))
    if len(nodes) == 0: raise Exception
    return nodes[0]


def select_colour(node: int, domain: Dict[int, Set[int]]) -> int:
    colour = domain[node].pop()
    return colour


def solution_breaks_constraint(assignment: Dict[int, int], edges: Dict[Tuple[int, int], bool]) -> bool:
    if len(assignment) < 2: return False
    if any([assignment.get(i) is not None and assignment.get(j) is not None and assignment[i] == assignment[j] for i, j in list(edges.keys())]): return True


def constraint_programming(node_count: int, edges: List[Tuple[int, int]]):
    """
    min( max(c[i]) ) = use the min nr of colours (colours are ints here).
    s.t. c[i] != c[j]
    """

    counter = Counter(map(itemgetter(0), edges))
    nodes = set(range(node_count))
    colours = set(range(node_count))
    domain = dict()
    nodes_selected = set()
    assignment = dict()
    nodes_sorted = counter.most_common() + [(x, 0) for x in nodes.difference(counter.keys())]
    edges_dict = defaultdict(bool)
    queue = deque(maxlen=node_count)

    for n in nodes:
        domain[n] = colours.copy()

    for i, j in edges:
        edges_dict[(i, j)] = True

    while True:

        if solution_breaks_constraint(assignment, edges_dict):
            n, c = queue.pop()
            nodes_selected.remove(n)
            assignment[n] = None
        else:
            if len(nodes_selected) == node_count: break
            n = None

        if n is None:
            # pick node
            n = select_node(nodes_sorted, nodes_selected)

        # pick colour
        c = select_colour(n, domain)

        queue.append((n, c))
        nodes_selected.add(n)
        assignment[n] = c

    solution_assignment = list(map(itemgetter(1), sorted(assignment.items())))
    solution_count = len(set(assignment.values()))

    return solution_count, solution_assignment
