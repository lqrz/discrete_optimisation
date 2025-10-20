from typing import List, Tuple, Dict, Set
from operator import itemgetter
from collections import Counter
from collections import deque
from collections import defaultdict
from plot.graph import plot_graph


def select_node(nodes_sorted: List[Tuple[int, int]], nodes_selected: Set[int]) -> int:
    nodes = list(filter(lambda x: x not in nodes_selected, map(itemgetter(0), nodes_sorted)))
    if len(nodes) == 0: raise Exception
    return nodes[0]


def select_colour(node: int, domain: Dict[int, Set[int]]) -> int:
    # select value
    c = min(domain[node])
    # remove from domain
    domain[node].remove(c)
    return c


class ConstraintStore:

    def __init__(self, edges: Dict[Tuple[int, int], bool], max_solution_count: int):
        self._edges = edges
        self._max_solution_count = max_solution_count

    def solution_breaks_constraint(self, assignment: Dict[int, int]) -> bool:
        # this is for the initial iterations
        if len(assignment) < 2: return False
        # c[i] != c[j]
        if any([assignment.get(i) is not None and assignment.get(j) is not None and assignment[i] == assignment[j] for i, j in list(self._edges.keys())]): return True
        if len(set((assignment.values()))) >= self._max_solution_count: return True
        return False


def _solve(nodes: Set[int], colours: Set[int], edges: Dict[Tuple[int, int], bool], constraint_store: ConstraintStore) -> Tuple[int, List[int]]:
    counter = Counter(map(itemgetter(0), edges))
    domain = dict()
    nodes_selected = set()
    assignment = dict()
    nodes_sorted = counter.most_common() + [(x, 0) for x in nodes.difference(counter.keys())]
    queue = deque(maxlen=len(nodes))

    for n in nodes:
        domain[n] = colours.copy()

    for i, j in edges:
        edges[(i, j)] = True

    while True:

        is_break_solution = constraint_store.solution_breaks_constraint(assignment)
        if is_break_solution:
            n, c = queue.pop()
            nodes_selected.remove(n)
            assignment[n] = None
            if len(domain[n]) == 0:
                if len(queue) == 0:
                    # cannot backtrack anymore
                    raise UnfeasibleError()
                else:
                    n2, c2 = queue.pop()
                    nodes_selected.remove(n2)
                    assignment[n2] = None
                    domain[n] = colours.copy()
                    n = n2
        else:
            if len(nodes_selected) == len(nodes): break
            n = None

        if n is None:
            # pick node
            n = select_node(nodes_sorted, nodes_selected)

        # pick colour
        c = select_colour(n, domain)

        queue.append((n, c))
        nodes_selected.add(n)
        assignment[n] = c

    solution_count = len(set(assignment.values()))
    solution_assignment = list(map(itemgetter(1), sorted(assignment.items())))

    return solution_count, solution_assignment


class UnfeasibleError(Exception):
    pass


def solve(node_count: int, edges: List[Tuple[int, int]]):
    """
    min( max(c[i]) ) = use the min nr of colours (colours are ints here).
    s.t. c[i] != c[j]
    """
    nodes = set(range(node_count))
    colours = set(range(node_count))

    # plot_graph(nodes=list(nodes), edges=edges)

    edges_dict = defaultdict(bool)
    for i, j in edges:
        edges_dict[(i, j)] = True

    print("Finding 1st solution")
    # find a solution
    constraint_store = ConstraintStore(edges=edges_dict, max_solution_count=node_count)
    # constraint_store = ConstraintStore(edges=edges_dict, max_solution_count=1)
    solution_count, solution_assignment = _solve(nodes=nodes, colours=colours, edges=edges_dict, constraint_store=constraint_store)
    print(f"First solution found: {solution_count}")

    while True:

        try:
            print("Finding new solution")
            # find the optimal solution
            constraint_store = ConstraintStore(edges=edges_dict, max_solution_count=solution_count)
            solution_count, solution_assignment = _solve(nodes=nodes, colours=colours, edges=edges_dict, constraint_store=constraint_store)
            print(f"New solution found: {solution_count}")
        except UnfeasibleError:
            print(f"Solution is already optimal: {solution_count}")
            break

    # plot_graph(nodes=list(nodes), edges=edges, colour_assignment=assignment)

    return solution_count, solution_assignment
