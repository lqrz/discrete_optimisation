import matplotlib.pyplot as plt
from utils import Customer, Facility
from typing import List


def plot(customers: List[Customer], facilities: List[Facility]):
    f, ax = plt.subplots(1, 1, figsize=(10, 10))
    _ = ax.scatter(x=[c.location[0] for c in customers],
                   y=[c.location[1] for c in customers],
                   c="blue",
                   s=50,
                   marker="o"
                   )
    _ = ax.scatter(x=[c.location[0] for c in facilities],
                   y=[c.location[1] for c in facilities],
                   c="red",
                   s=60,
                   marker="x"
                   )
    plt.show()
