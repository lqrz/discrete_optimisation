from ortools.linear_solver import pywraplp
from typing import List, Tuple
from utils import Point, length
from itertools import combinations, product
from plot import plot_graph


def _get_node_pairs(node_count: int) -> List[Tuple[int, int]]:
    return filter(lambda x: x[0] != x[1], [(i, j) for i in range(node_count) for j in range(node_count)])


def solve(points: List[Point]) -> List[int]:

    points_ixs = dict(zip(range(len(points)), points))

    # instantiate solver
    solver = pywraplp.Solver.CreateSolver('SAT')

    node_count = len(points)

    # create variables
    variables = dict()

    for i, j in _get_node_pairs(node_count):
        variables[(i, j)] = solver.IntVar(lb=0, ub=1, name=f"{i}_{j}")

    # constraints: visit all cities
    solver.Add(sum([variables[x] for x in _get_node_pairs(node_count)]) == node_count)

    # constraints: one-way
    for x in combinations(range(node_count), 2):
        solver.Add(variables[x[0], x[1]] + variables[x[1], x[0]] <= 1)

    # constraints: one outbound
    for i in range(node_count):
        solver.Add(sum([variables[(i, j)] for j in range(node_count) if i != j]) == 1)

    # constraints: one inbound
    for i in range(node_count):
        solver.Add(sum([variables[(j, i)] for j in range(node_count) if i != j]) == 1)

    # constraints: isolated routed
    variables_time = dict()
    for i in range(1, node_count):
        variables_time[i] = solver.NumVar(lb=1, ub=solver.infinity(), name=f"id_city_{i}")

    for i, j in filter(lambda x: x[0] != x[1] , product(range(1, node_count), range(1, node_count))):
        solver.Add( variables_time[j] >= variables_time[i] + 1 - (2 * node_count) * (1 - variables[(i, j)]))

    # objective function
    solver.Minimize(sum(map(lambda x: variables[x] * length(points_ixs[x[0]], points_ixs[x[1]]), _get_node_pairs(node_count))))

    # solve
    status = solver.Solve()

    print(f"Status: {status}")

    if status == pywraplp.Solver.OPTIMAL:
        value = solver.Objective().Value()
        print(f"Value: {value}")
        # for k, v in variables.items():
        #     print(f"{k}: {v.solution_value()}")

        # get path
        ix_initial = 0
        path = [ix_initial]
        ix = ix_initial
        while True:
            ix = [j for j in range(node_count) if ix != j and variables[(ix, j)].solution_value() == 1][0]
            if ix == ix_initial: break
            path.append(ix)

        # plot_graph(points=points, edges=list(filter(lambda x: variables[(x[0], x[1])].solution_value() == 1, _get_node_pairs(node_count))))

        return path
    else:
        raise Exception("No solution")



# def solve(points: List[Point]) -> List[int]:
#
#     points_ixs = dict(zip(range(len(points)), points))
#
#     # instantiate solver
#     solver = pywraplp.Solver.CreateSolver('SAT')
#
#     node_count = len(points)
#
#     # create variables
#     variables = dict()
#     variables[(0, 1)] = solver.IntVar(lb=0, ub=1, name="0_1")
#     variables[(0, 2)] = solver.IntVar(lb=0, ub=1, name="0_2")
#     variables[(0, 3)] = solver.IntVar(lb=0, ub=1, name="0_3")
#     variables[(1, 0)] = solver.IntVar(lb=0, ub=1, name="1_0")
#     variables[(1, 2)] = solver.IntVar(lb=0, ub=1, name="1_2")
#     variables[(1, 3)] = solver.IntVar(lb=0, ub=1, name="1_3")
#     variables[(2, 0)] = solver.IntVar(lb=0, ub=1, name="2_0")
#     variables[(2, 1)] = solver.IntVar(lb=0, ub=1, name="2_1")
#     variables[(2, 3)] = solver.IntVar(lb=0, ub=1, name="2_3")
#     variables[(3, 0)] = solver.IntVar(lb=0, ub=1, name="3_0")
#     variables[(3, 1)] = solver.IntVar(lb=0, ub=1, name="3_1")
#     variables[(3, 2)] = solver.IntVar(lb=0, ub=1, name="3_2")
#
#     # constraints: visit all cities
#     solver.Add(
#         variables[(0, 1)] +
#         variables[(0, 2)] +
#         variables[(0, 3)] +
#         variables[(1, 0)] +
#         variables[(1, 2)] +
#         variables[(1, 3)] +
#         variables[(2, 0)] +
#         variables[(2, 1)] +
#         variables[(2, 3)] +
#         variables[(3, 0)] +
#         variables[(3, 1)] +
#         variables[(3, 2)] == 4)
#
#     # constraints: one-way
#     solver.Add(variables[(0, 1)] + variables[(1, 0)] <= 1)
#     solver.Add(variables[(0, 2)] + variables[(2, 0)] <= 1)
#     solver.Add(variables[(0, 3)] + variables[(3, 0)] <= 1)
#     solver.Add(variables[(1, 2)] + variables[(2, 1)] <= 1)
#     solver.Add(variables[(1, 3)] + variables[(3, 1)] <= 1)
#     solver.Add(variables[(2, 3)] + variables[(3, 2)] <= 1)
#
#     # constraints: one outbound
#     solver.Add(sum(map(lambda x: variables[x], [(0, 1), (0, 2), (0, 3)])) == 1)
#     solver.Add(sum(map(lambda x: variables[x], [(1, 0), (1, 2), (1, 3)])) == 1)
#     solver.Add(sum(map(lambda x: variables[x], [(2, 0), (2, 1), (2, 3)])) == 1)
#     solver.Add(sum(map(lambda x: variables[x], [(3, 0), (3, 1), (3, 2)])) == 1)
#
#     # constraints: one inbound
#     solver.Add(sum(map(lambda x: variables[x], [(1, 0), (2, 0), (3, 0)])) == 1)
#     solver.Add(sum(map(lambda x: variables[x], [(0, 1), (2, 1), (3, 1)])) == 1)
#     solver.Add(sum(map(lambda x: variables[x], [(0, 2), (1, 2), (3, 2)])) == 1)
#     solver.Add(sum(map(lambda x: variables[x], [(0, 3), (1, 3), (2, 3)])) == 1)
#
#     solver.Minimize(
#         variables[(0, 1)] * length(points_ixs[0], points_ixs[1]) +
#         variables[(0, 2)] * length(points_ixs[0], points_ixs[2]) +
#         variables[(0, 3)] * length(points_ixs[0], points_ixs[3]) +
#         variables[(1, 0)] * length(points_ixs[1], points_ixs[0]) +
#         variables[(1, 2)] * length(points_ixs[1], points_ixs[2]) +
#         variables[(1, 3)] * length(points_ixs[1], points_ixs[3]) +
#         variables[(2, 0)] * length(points_ixs[2], points_ixs[0]) +
#         variables[(2, 1)] * length(points_ixs[2], points_ixs[1]) +
#         variables[(2, 3)] * length(points_ixs[2], points_ixs[3]) +
#         variables[(3, 0)] * length(points_ixs[3], points_ixs[0]) +
#         variables[(3, 1)] * length(points_ixs[3], points_ixs[1]) +
#         variables[(3, 2)] * length(points_ixs[3], points_ixs[2])
#     )
#
#     # solve
#     status = solver.Solve()
#
#     print(f"Status: {status}")
#
#     if status == pywraplp.Solver.OPTIMAL:
#         value = solver.Objective().Value()
#         print(f"Value: {value}")
#         for k, v in variables.items():
#             print(f"{k}: {v.solution_value()}")
