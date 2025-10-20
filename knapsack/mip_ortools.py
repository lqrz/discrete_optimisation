from ortools.linear_solver import pywraplp
from typing import List
from item import Item


def solve(items: List[Item], capacity: int):
    solver = pywraplp.Solver.CreateSolver('SAT')
    item_variables = dict()
    for x in items:
        item_variables[x.index] = solver.IntVar(lb=0, ub=1, name=str(x.index))

    solver.Add(sum([x.weight * item_variables[x.index] for x in items]) <= capacity)

    solver.Maximize(sum([x.value * item_variables[x.index] for x in items]))
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        value = int(solver.Objective().Value())
        taken = [int(x.solution_value()) for x in item_variables.values()]
        sum_weight = sum([x.weight * int(item_variables[x.index].solution_value()) for x in items])
        print(f"Capacity: {capacity} Weight: {sum_weight}")
        return value, taken
    else:
        raise Exception("No solution")