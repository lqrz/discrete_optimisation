from typing import List, Tuple
from utils import Point, length
from plot import plot_graph


def solve(points: List[Point], initial_point: int) -> List[int]:
    node_count = len(points)
    points_ixs = dict(zip(range(len(points)), points))

    i = initial_point
    points_to_select = set(range(len(points)))
    points_to_select.remove(i)
    path = [i]
    while True:
        if len(points_to_select) == 0: break
        lens = [(j, length(points_ixs[i], points_ixs[j])) for j in points_to_select]
        greedy_j = sorted(lens, key=lambda x: x[1])[0][0]
        path.append(greedy_j)
        points_to_select.remove(greedy_j)

    # edges = list(zip(path, path[1:])) + [(path[-1], path[0])]
    # plot_graph(points=points, edges=edges)

    return path
