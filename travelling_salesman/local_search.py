from typing import List, Callable, Tuple
from utils import Point, length
import greedy as gd
import numpy as np
from Neighbours import Neighbours
from operator import itemgetter


def load_from_file(path_input):
    return list(map(int, open("solutions/1889").read().split(" ")))


def _get_initial_solution(points: List[Point], initial_point: int) -> List[int]:
    # return gd.solve(points=points, initial_point=initial_point)
    return load_from_file("solutions/1889")


def _get_random_neighbour(neighbours_model: Neighbours, point: Point, k: int, points_ixs):
    # get neighbours to that point
    # indices correspond to points_ixs
    options, options_ixs = neighbours_model.get_neighbours(point=point, k=k)
    # select a point from those neighbours
    # this ix corresponds to the options array
    ix_from_options = np.random.choice(len(options), 1)[0]
    # this ix corresponds to points_ixs
    ix = options_ixs[ix_from_options]
    point_neighbour = options[ix_from_options]
    return ix, point_neighbour


def select_points_to_swap_from_neighbours(solution, neighbours_model, k_candidates, k_neighbours, threshold_distance, points_ixs):
    while True:

        # select a point from the solution
        # this ix_1 corresponds to the solution array
        # --- from top longest
        if k_candidates is not None:
            options = sorted(compute_path_lengths(solution=solution, points_ixs=points_ixs), key=itemgetter(1), reverse=True)[:k_candidates]
            ix_1, _ = options[np.random.choice(len(options))]
        else:
            # --- randomly
            ix_1 = np.random.choice(len(solution))

        # if ix_1 + 1 == len(solution): continue
        # this ix_2 corresponds to the points_ixs
        ix_2, p2 = _get_random_neighbour(point=points_ixs[solution[ix_1]], neighbours_model=neighbours_model, k=k_neighbours, points_ixs=points_ixs)

        # do not select the same point
        if ix_1 == ix_2: continue
        # do not select adjacent points
        p1_end = 0 if ix_1 + 1 == len(solution) else solution[ix_1 + 1]
        if p1_end == ix_2: continue
        # min distance threshold
        if length(points_ixs[ix_1], points_ixs[ix_2]) > threshold_distance: break
    return sorted([solution[ix_1], solution[ix_2]])


def select_points_to_swap_randomly(solution, threshold_distance, points_ixs, *args, **kwargs):
    while True:
        ix_1, ix_2 = sorted(np.random.choice(len(solution), 2))
        # do not select the same point
        if ix_1 == ix_2: continue
        # do not select adjacent points
        if solution[ix_1 + 1] == solution[ix_2]: continue
        # min distance threshold
        if length(points_ixs[ix_1], points_ixs[ix_2]) > threshold_distance: break
    return sorted([solution[ix_1], solution[ix_2]])


def fix_solution(solution, p1, p2):
    assert p1 < p2
    # try:
    ix_1 = np.array(solution)[np.array(solution) == p1][0]
    ix_2 = np.array(solution)[np.array(solution) == p2][0]
    # except:
    #     print("debug")
    solution_fixed = solution[:ix_1+1] + solution[ix_1+1:ix_2+1][::-1] + solution[ix_2+1:]
    # if len(solution_fixed) > len(set(solution_fixed)):
    #     print("debug")
    return solution_fixed


def compute_path_lengths(solution, points_ixs) -> List[Tuple[int, float]]:
    lens = list(map(lambda x: length(points_ixs[x[0]], points_ixs[x[1]]), zip(solution, solution[1:]))) + [length(points_ixs[solution[-1]], points_ixs[solution[0]])]
    return list(zip(solution, lens))


def score(solution, points_ixs):
    lens = compute_path_lengths(solution=solution, points_ixs=points_ixs)
    return sum(map(itemgetter(1), lens))


def metropolis(original, temperature, threshold_distance, points_ixs, neighbours_model, k_candidates, k_neighbours, f_swap: Callable):
    p1, p2 = f_swap(solution=original, neighbours_model=neighbours_model, k_candidates=k_candidates, k_neighbours=k_neighbours, threshold_distance=threshold_distance, points_ixs=points_ixs)
    solution_new = fix_solution(original, p1, p2)
    score_original = score(original, points_ixs)
    score_new = score(solution_new, points_ixs)
    is_exploration = False
    is_swap = False
    if score_new < score_original:
        is_swap = True
        return solution_new, score_new, is_swap, is_exploration
    p = np.random.random()
    score_diff = score_new - score_original
    threshold_prob = np.exp(-score_diff / temperature)
    # print(f"Score diff: {score_diff}")
    # print(f"P: {p} threshold: {threshold_prob}")
    if p <= threshold_prob:
        is_swap = True
        is_exploration = True
        return solution_new, score_new, is_swap, is_exploration
    return original, score_original, is_swap, is_exploration


def solve(points: List[Point]) -> List[int]:
    neighbours_model = Neighbours(points=points)
    # return solve_with_restarts(points=points)
    return solve_one_iteration(points=points, initial_point=0, neighbours_model=neighbours_model)


def solve_with_restarts(points: List[Point], neighbours_model: Neighbours) -> List[int]:
    n_restarts = 10
    path_best, score_best = [], np.inf
    for _ in range(n_restarts):
        ix_start = np.random.choice(len(points))
        path, score = solve_one_iteration(points=points, initial_point=ix_start)
        if score < score_best:
            print(f"Best score: {score}")
            path_best = path
            score_best = score
    return path_best


def solve_one_iteration(points: List[Point], initial_point: int, neighbours_model: Neighbours) -> List[int]:
    node_count = len(points)
    points_ixs = dict(zip(range(len(points)), points))

    path_initial = _get_initial_solution(points=points, initial_point=initial_point)
    score_initial = score(path_initial, points_ixs)

    # f_swap = select_points_to_swap_randomly
    f_swap = select_points_to_swap_from_neighbours

    # potential swap vecinity
    k_candidates = 10
    k_candidates = None
    k_neighbours = 30
    # temperature = 10
    temperature = 200
    # threshold_distance = sum(map(lambda x: length(points_ixs[x[0]], points_ixs[x[1]]), zip(path_initial, path_initial[1:]))) / (len(points) - 1 )
    threshold_distance = 0

    # potential swap vecinity
    k_candidates = 10
    # k_candidates = None
    k_neighbours = 300
    # temperature = 10
    temperature = 50
    # threshold_distance = sum(map(lambda x: length(points_ixs[x[0]], points_ixs[x[1]]), zip(path_initial, path_initial[1:]))) / (len(points) - 1 )
    threshold_distance = 0

    print(f"Score initial: {score_initial}")
    score_best = score_initial
    path_best = path_initial
    n_rounds = 1000000
    # if node_count >= 574:
    #     n_rounds = 1000000
    #     temperature = .75
    path = path_initial
    swaps = []
    explorations = []
    for i in range(n_rounds):
        # select_points_to_swap(path, threshold, points_ixs)
        path, score_new, is_swap, is_exploration = metropolis(path, temperature, threshold_distance=threshold_distance, points_ixs=points_ixs, neighbours_model=neighbours_model, k_candidates=k_candidates, k_neighbours=k_neighbours, f_swap=f_swap)
        swaps.append(is_swap)
        explorations.append(is_exploration)
        # print(f"Score: {score_new}")
        if i % 10000 == 0:
            print(f"Swaps: {np.mean(swaps)} Explorations: {np.mean(explorations)}")
        if score_new < score_best:
            print(f"Best score: {score_new}")
            score_best = score_new
            path_best = path

    print(f"Final score: {score_best}")

    return path_best
