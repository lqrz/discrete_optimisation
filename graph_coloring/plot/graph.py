import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional, Dict
import seaborn as sns


def _create_palette(n: int) -> List[str]:
    return sns.color_palette("Set2", n)


def plot_graph(nodes: List[int], edges: List[Tuple[int, int]]) -> None:
    # create graph
    g = nx.Graph()
    # add nodes
    g.add_nodes_from(nodes)
    # add edges
    g.add_edges_from(edges)
    # plot
    nx.draw(g, with_labels=True, font_weight='bold', alpha=.8)
    plt.show()
