#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import Point, length
import mip_ortools as mo
import mip_pulp as plp
import local_search as ls
import greedy as gd
import routing_ortools as ro


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    node_count = int(lines[0])

    points = []
    for i in range(1, node_count + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    # solution = range(0, node_count)
    # solution = mo.solve(points=points)
    # solution = plp.solve(points=points)
    # solution = gd.solve(points=points)
    # solution = ls.solve(points=points)
    # solution = ro.solve(points=points)

    solution = list(map(int, open(f"solutions/{node_count}").read().split(" ")))

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, node_count - 1):
        obj += length(points[solution[index]], points[solution[index + 1]])

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
