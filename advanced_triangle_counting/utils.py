import random

import networkx as nx
from networkx import is_empty


def load_graph_from_file(path):
    fh = open(path, "rb")
    G = nx.read_edgelist(fh)

    return G


def stream_edge(G, remove=True):
    """
    Reads a random edge from a graph and then removes it, to simulate streaming
    Notice: The graph needs to fit in memory for this method to work
    :return:
    """
    if is_empty(G):
        return None, ()
    edge = random.sample(G.edges(), 1)[0]
    node_a, node_b = edge
    if remove:
        G.remove_edge(node_a, node_b)

    return G, edge
