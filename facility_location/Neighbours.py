from sklearn.neighbors import KDTree
from typing import List
from utils import Customer, Facility
from operator import attrgetter


class Neighbours:

    def __init__(self, customers: List[Customer], leaf_size: int = 30):
        self._customers = customers
        coords = list(map(attrgetter("location"), self._customers))
        self._model = KDTree(coords, leaf_size=leaf_size, metric='euclidean')

    def get_neighbours(self, facility: Facility, k: int) -> List[int]:
        ixs = self._model.query([[facility.location[0], facility.location[1]]], k=k, return_distance=False)[0][1:]
        # neighbours = [c for c in self._customers if c.index in ixs]
        return ixs
