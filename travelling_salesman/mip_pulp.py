from typing import List, Tuple
from utils import Point, length
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value


def solve(points: List[Point]) -> List[int]:
    node_count = len(points)
    points_ixs = dict(zip(range(len(points)), points))

    model = LpProblem('tsp', LpMinimize)

    # variables
    x = LpVariable.dicts("x", ((i, j) for i in range(node_count) for j in range(node_count)), cat='Binary')
    t = LpVariable.dicts("t", (i for i in range(node_count)), lowBound=1, upBound=node_count, cat='Continuous')

    # objective
    model += lpSum(x[i, j] * length(points_ixs[i], points_ixs[j]) for i in range(node_count) for j in range(node_count))

    # constraints
    for i in range(node_count):
        model += x[i, i] == 0
        model += lpSum(x[i, j] for j in range(node_count)) == 1
        model += lpSum(x[j, i] for j in range(node_count)) == 1

    # eliminate subtour
    for i in range(node_count):
        for j in range(node_count):
            if i != j and (i != 0 and j != 0):
                model += t[j] >= t[i] + 1 - (2 * node_count) * (1 - x[i, j])

    status = model.solve()

    print("-----------------")
    print(status, LpStatus[status], value(model.objective))
    route = [(i, j) for i in range(node_count) for j in range(node_count) if value(x[i, j]) == 1]
    print(route)
