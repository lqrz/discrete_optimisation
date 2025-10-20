#!/usr/bin/python
# -*- coding: utf-8 -*-
import constraint_programming as cp
import linear_programming as lp


def trivial_solution(node_count:int):
    """
    build a trivial solution.
    every node has its own color.
    """
    return node_count, range(0, node_count)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # colours_cnt, colours_assignment = trivial_solution(node_count)
    colours_cnt, colours_assignment = cp.solve(node_count, edges)
    # colours_cnt, colours_assignment = lp.solve(node_count, edges)

    # prepare the solution in the specified output format
    output_data = str(colours_cnt) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, colours_assignment))

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.')
