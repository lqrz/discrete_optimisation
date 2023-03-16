from typing import List
from collections import defaultdict
import numpy as np
from item import Item


def dynamic_programming_naive(items: List[Item], capacity: int):
    value_function = defaultdict(lambda: defaultdict(lambda: 0))
    pointers = defaultdict(lambda: defaultdict(lambda: []))
    weight_min = min(map(lambda x: x.weight, items))

    # iterate one item at a time (order does not matter)
    for ix_item, item in enumerate(items):
        # all capacities < weight_min will be zero
        for c in range(weight_min, capacity + 1):
            # fits
            if item.weight <= c:
                previous_value = value_function[c][ix_item]
                actual_value = item.value + value_function[c - item.weight][ix_item]
                if actual_value > previous_value:
                    # take it
                    value_function[c][ix_item + 1] = actual_value
                    pointers[c][ix_item + 1] = pointers[c - item.weight][ix_item] + [item.index]
                else:
                    # do not take it
                    value_function[c][ix_item + 1] = previous_value
                    pointers[c][ix_item + 1] = pointers[c][ix_item]
            else:
                # does not fit
                value_function[c][ix_item + 1] = value_function[c][ix_item]
                pointers[c][ix_item + 1] = pointers[c][ix_item]

    value = max(value_function[c].values())

    # get item indexes
    ix_argmax = np.argmax(list(value_function[c].values()))
    taken = np.array([0] * len(items))
    taken[pointers[c][ix_argmax]] = 1

    return value, taken


def dynamic_programming_memoisation_optimised(items: List[Item], capacity: int):
    value_function = defaultdict(lambda: 0)
    pointers = defaultdict(lambda: [])
    weight_min = min(map(lambda x: x.weight, items))

    # iterate one item at a time (order does not matter)
    for ix_item, item in enumerate(items):

        # all capacities < weight_min will be zero
        for c in range(weight_min, capacity + 1):
            # fits
            if item.weight <= c:
                previous_value = value_function[c]#[ix_item]
                actual_value = item.value + value_function[c - item.weight][ix_item]
                if actual_value > previous_value:
                    # take it
                    value_function[c][ix_item + 1] = actual_value
                    pointers[c][ix_item + 1] = pointers[c - item.weight][ix_item] + [item.index]
                else:
                    # do not take it
                    value_function[c][ix_item + 1] = previous_value
                    pointers[c][ix_item + 1] = pointers[c][ix_item]
            else:
                # does not fit
                value_function[c][ix_item + 1] = value_function[c][ix_item]
                pointers[c][ix_item + 1] = pointers[c][ix_item]

    value = max(value_function[c].values())

    # get item indexes
    ix_argmax = np.argmax(list(value_function[c].values()))
    taken = np.array([0] * len(items))
    taken[pointers[c][ix_argmax]] = 1

    return value, taken
