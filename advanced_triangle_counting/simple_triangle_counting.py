import networkx as nx


def count_triangles(G):
    return int(sum(nx.triangles(G).values()) / 3)
