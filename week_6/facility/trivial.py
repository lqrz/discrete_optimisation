from typing import List
from utils import Customer, Facility, length


def solve(customers: List[Customer], facilities: List[Facility]):
    # build a trivial solution
    # pack the facilities one by one until all the customers are served
    solution = [-1] * len(customers)
    capacity_remaining = [f.capacity for f in facilities]

    facility_index = 0
    for customer in customers:
        if capacity_remaining[facility_index] >= customer.demand:
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand
        else:
            facility_index += 1
            assert capacity_remaining[facility_index] >= customer.demand
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand

    used = [0] * len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    cost = sum([f.setup_cost * used[f.index] for f in facilities])
    for customer in customers:
        cost += length(customer.location, facilities[solution[customer.index]].location)

    return solution, cost
