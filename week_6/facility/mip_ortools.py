from typing import List, Optional
from utils import Customer, Facility, length
from ortools.linear_solver import pywraplp
import numpy as np
from Neighbours import Neighbours


def solve(customers: List[Customer],
          facilities: List[Facility],
          n_max_facilities: Optional[int] = None,
          n_xs: int = 1,
          n_ys: int = 1):
    # subdivide the problem
    xs = [c.location.x for c in customers]
    ys = [c.location.y for c in customers]

    linspace_x = np.linspace(start=min(xs), stop=max(xs), num=n_xs)
    linspace_y = np.linspace(start=min(ys), stop=max(ys), num=n_ys)

    # fix borders
    linspace_x = linspace_x + ([0] * (linspace_x.shape[0] - 1) + [1])
    linspace_y = linspace_y + ([0] * (linspace_y.shape[0] - 1) + [1])

    solution = []
    cost = 0

    for ix in range(len(linspace_y) - 1):
        y_min, y_max = linspace_y[ix:ix + 2]
        for ix in range(len(linspace_x) - 1):
            x_min, x_max = linspace_x[ix:ix + 2]
            customers_subproblem = [c for c in customers
                                    if c.location.x >= x_min and
                                    c.location.x < x_max and
                                    c.location.y >= y_min and
                                    c.location.y < y_max]
            facilities_subproblem = [f for f in facilities
                                     if f.location.x >= x_min and
                                     f.location.x < x_max and
                                     f.location.y >= y_min and
                                     f.location.y < y_max]
            demand_subproblem = sum([c.demand for c in customers_subproblem])
            capacity_subproblem = sum([f.capacity for f in facilities_subproblem])
            n_nec_facilities = int(np.ceil(capacity_subproblem / demand_subproblem))
            print("N customers", len(customers_subproblem))
            print("N facilities", len(facilities_subproblem))
            print("Demand", demand_subproblem)
            print("Capacity", capacity_subproblem)
            print("Necessary facilities", n_nec_facilities)
            solution_subproblem, cost_subproblem = solve_subproblem(customers=customers_subproblem,
                                                                    facilities=facilities_subproblem,
                                                                    n_max_facilities=n_max_facilities)
            cost += cost_subproblem
            solution.extend(solution_subproblem)

    solution = list(map(lambda x: x[1], sorted(solution, key=lambda x: x[0])))
    return solution, cost


def solve_subproblem(customers: List[Customer],
                     facilities: List[Facility],
                     n_max_facilities: Optional[int] = None):
    # --- solver
    solver = pywraplp.Solver.CreateSolver('SAT')

    # --- variables

    variables = dict()
    for c in customers:
        for f in facilities:
            variables[(c.index, f.index)] = solver.IntVar(lb=0, ub=1, name=f"{c.index}_{f.index}")

    variables_facilities = dict()
    for f in facilities:
        variables_facilities[(f.index)] = solver.IntVar(lb=0, ub=1, name=f"{f.index}")

    # --- constraints

    # can only serve a customer if open
    for f in facilities:
        for c in customers:
            solver.Add(variables[(c.index, f.index)] <= variables_facilities[f.index])

    # only one facility per customer
    for c in customers:
        solver.Add(sum([variables[(c.index, f.index)] for f in facilities]) == 1)

    # capacity
    for f in facilities:
        solver.Add(sum([c.demand * variables[(c.index, f.index)] for c in customers]) <= f.capacity)

    # limit the max nr of open facilities
    # useful for problem 4
    if n_max_facilities is not None:
        solver.Add(sum([variables_facilities[f.index] for f in facilities]) == n_max_facilities)

    # # neighbourhood
    # neighbours_model = Neighbours(customers=customers)
    # for f in facilities:
    #     neighbours_ixs = neighbours_model.get_neighbours(facility=f, k=80)
    #     for c in customers:
    #         if c.index not in neighbours_ixs:
    #             solver.Add(variables[(c.index, f.index)] == 0)

    # --- objective function

    # setup_cost
    cost = sum([f.setup_cost * variables_facilities[f.index] for f in facilities])
    for f in facilities:
        # distances
        cost += sum([length(c.location, f.location) * variables[(c.index, f.index)] for c in customers])

    solver.Minimize(cost)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        cost = int(solver.Objective().Value())
        solution = []
        for c in customers:
            solution.append(
                (c.index,
                 [f.index for f in facilities if variables[(c.index, f.index)].solution_value() == 1][0]
                 )
            )
        print(f"Cost: {cost}")
        return solution, cost
    else:
        raise Exception("No solution")
