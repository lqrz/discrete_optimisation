from typing import List
from item import Item


# def compute_relaxation_optimal(items: List[Item]):
#     return sum([x.value for x in items])
#
#
# def get_remaining_items(items: List[Item], item:Item):
#     return [x for x in items if x.index != item.index]
#
#
# def branch_and_bound(items: List[Item], capacity: int, value_max: int, value_acc: int = 0, items_selected: List[Item] = []):
#
#     # capacity
#     if capacity < 0: return None, None
#
#     # estimate if picked
#     relaxation_value = value_acc + compute_relaxation_optimal(items)
#     if relaxation_value < value_max: return None, None
#
#     if len(items) == 0: return value_acc, items_selected
#
#     # leaf node
#     capacity_remaining = capacity - items[0].weight
#     # if len(items) == 1 and capacity_remaining >= 0:
#     #     # take
#     #     value = items[0].value + value_acc
#     #     return value, items_selected + [items[0]]
#
#     # middle node
#     items_remaining = get_remaining_items(items=items, item=items[0])
#     # branch left
#     items_selected_left = items_selected + [items[0]]
#     value_left, items_selected_left = branch_and_bound(items=items_remaining, capacity=capacity_remaining, value_max=items[0].value + value_acc, value_acc=value_acc + items[0].value, items_selected=items_selected_left)
#     # branch right
#     if [x.index for x in items_remaining] == [2,3]:
#         print('debug')
#     value_max_right = max(filter(lambda x: x is not None, [value_max, value_acc, value_left]))
#     value_right, items_selected_right = branch_and_bound(items=items_remaining, capacity=capacity, value_max=value_max_right, value_acc=value_acc, items_selected=items_selected)
#
#     if value_left is not None and value_right is not None:
#         if value_left > value_right:
#             return value_left, items_selected_left
#         else:
#             return value_right, items_selected_right
#
#     if value_left is not None:
#         return value_left, items_selected_left
#
#     if value_right is not None:
#         return value_right, items_selected_right
#
#     return value_acc, items_selected
