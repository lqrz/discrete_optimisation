from ortools.sat.python import cp_model
from typing import Set, List, Tuple
# import signal
import func_timeout
#
# class TimeoutException(Exception):   # Custom exception class
#     pass
#
#
# def timeout_handler(*args, **kwargs):   # Custom signal handler
#     raise TimeoutException


def solve(node_count: int, edges: List[Tuple[int, int]]):

    nodes = set(range(node_count))
    colours = set(range(node_count))

    colours_cnt = 0
    n_assigned_colours_max = len(nodes)
    n_assigned_colours_max = 120
    # signal.signal(signal.SIGALRM, timeout_handler)

    while True:
        # n_assigned_colours_max = len(nodes)
        # n_assigned_colours_max = 0
        print(f"Trying max count: {n_assigned_colours_max}")

        timeout = 60 * 5
        # signal.alarm(1)
        # _solve(nodes=nodes, colours=colours, edges=edges, n_assigned_colours_max=n_assigned_colours_max)
        try:
            colours_cnt_i, colours_assignment_i = func_timeout.func_timeout(timeout, _solve, kwargs={"nodes":nodes, "colours":colours, "edges":edges, "n_assigned_colours_max":n_assigned_colours_max})
        # except TimeoutException:
        except func_timeout.FunctionTimedOut:
            print("killed")
            break
        else:
            # signal.alarm(0)
            if colours_cnt_i is None:
                break
            colours_cnt, colours_assignment = colours_cnt_i, colours_assignment_i
            n_assigned_colours_max = colours_cnt_i - 2

    return colours_cnt, colours_assignment


def _solve(nodes: Set[int], colours: Set[int], edges: List[Tuple[int, int]], n_assigned_colours_max: int):
    # model
    model = cp_model.CpModel()

    # variables
    assignment = dict()
    for n in nodes:
        assignment[n] = model.NewIntVar(lb=min(colours), ub=n_assigned_colours_max, name=f"node_{n}")

    # constraints
    for n1, n2 in edges:
        model.Add(assignment[n1] != assignment[n2])

    from collections import Counter
    from operator import itemgetter
    edges_reversed = [(y, x) for x, y in edges]
    counter = Counter(map(itemgetter(0), edges + edges_reversed))
    node_most_common = counter.most_common(1)[0][1]

    model.Add(assignment[node_most_common] == 0)

    # # minimisation constraint
    # assigned_colours = []
    #

    # model.Add(len(set(assignment.values())) < 50)
    # n_assigned_colours = max(assignment.values())
    # model.Add(n_assigned_colours < n_assigned_colours_max)

    # solver
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = False

    colours_cnt, colours_assignment = None, []
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        colours_assignment = [solver.Value(assignment[n]) for n in nodes]
        colours_cnt = max(colours_assignment) + 1

    return colours_cnt, colours_assignment
