#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *
import trivial as tv
import mip_ortools as mp
from plot import plot


def read_data(input_data):
    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    facilities = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3]))))

    customers = []
    for i in range(facility_count + 1, facility_count + 1 + customer_count):
        parts = lines[i].split()
        customers.append(Customer(i - 1 - facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    return customers, facilities


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    customers, facilities = read_data(input_data)

    facility_count = len(facilities)
    customer_count = len(customers)

    # plot(customers=customers, facilities=facilities)

    n_max_facilities = None
    if facility_count == 100 and customer_count == 1000:
        # problem 4
        n_max_facilities = 7

    n_xs, n_ys = 2, 2
    if facility_count == 200 and customer_count == 800:
        # problem 5
        n_xs, n_ys = 3, 3
    if facility_count == 500 and customer_count == 3000:
        # problem 6
        n_xs, n_ys = 6, 6
    if facility_count == 1000 and customer_count == 1500:
        # problem 7
        n_xs, n_ys = 7, 7
    if facility_count == 2000 and customer_count == 2000:
        # problem 8
        n_xs, n_ys = 10, 10

    # solution, cost = tv.solve(customers=customers, facilities=facilities)

    solution, cost = mp.solve(customers=customers, facilities=facilities,
                              n_max_facilities=n_max_facilities,
                              n_xs=n_xs, n_ys=n_ys)

    # prepare the solution in the specified output format
    output_data = '%.2f' % cost + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')
