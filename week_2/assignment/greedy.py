from typing import List
from item import Item


def greedy(items: List[Item], capacity: int):
    value = 0
    weight = 0
    taken = [0] * len(items)
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return value, taken


def greedy_optimised(items: List[Item], capacity: int):
    value = 0
    weight = 0
    taken = [0] * len(items)
    items_sorted = sorted(items, key=lambda x: x.value / x.weight, reverse=True)
    for item in items_sorted:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return value, taken
