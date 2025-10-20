import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple
from utils import Point


def plot_graph(points: List[Point], edges: List[Tuple[int, int]]) -> None:
    # create graph
    g = nx.Graph()
    # add nodes
    g.add_nodes_from(range(len(points)))
    # add edges
    g.add_edges_from(edges)
    # plot
    pos = dict([(ix, (x, y)) for ix, (x, y) in enumerate(points)])
    nx.draw(g, pos=pos, with_labels=True, font_weight='bold', alpha=.8)
    plt.show()
