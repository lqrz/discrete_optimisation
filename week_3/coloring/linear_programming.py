from pulp import LpVariable, LpProblem, LpMinimize, LpInteger, lpSum
from typing import List, Tuple


def solve(node_count: int, edges: List[Tuple[int, int]]):
    nodes = set(range(node_count))
    colours = set(range(node_count))
    variables = dict()

    assignment = LpVariable.dicts("assignment", nodes, lowBound=0, upBound=len(colours), cat="LpInteger")

    # # instantiate variables
    # for n in nodes:
    #     variables[n] = LpVariable(n, 0, len(colours), LpInteger)

    # instantiate problem
    problem = LpProblem("colouring", LpMinimize)

    # add objective
    problem += max([assignment[n] for n in nodes])

    from collections import defaultdict
    edges_dict = defaultdict(list)
    for n1, n2 in edges:
        edges_dict[n1].append(n2)

    # add constraints
    for node, neighbours in edges_dict.items():
        problem += lpSum([assignment[node] != assignment[n] for n in neighbours])

    # solve
    status = problem.solve()

    for v in problem.variables():
        print(v.name, "=", v.varValue)