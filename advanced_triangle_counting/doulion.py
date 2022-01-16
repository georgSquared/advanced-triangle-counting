import networkx as nx
import numpy as np
import random
from random import randint
import pandas as pd
import time
from itertools import combinations


def doulion_node_iterator(G, p=0.9):
    for e1, e2 in G.edges:
        random.seed(10)
        r1 = random.uniform(0, 1)
        if r1 < p:
            nx.set_edge_attributes(G, {(e1, e2): {"weight": 1 / p}})
        else:
            G.remove_edge(e1, e2)

    # triangle counter
    tc = 0
    # for v belongs V do
    for v in G.nodes:
        # list of neighbors
        nei = []
        # for all pairs of Neighbors {u,w} of v do
        for u in G.neighbors(v):
            nei.append(u)
        # pairs of 2 of neighbors
        nei2 = list(combinations(nei, 2))
        for i in range(0, len(nei2)):
            if nei2[i] in G.edges():
                # sort my tuples in ascending order
                result = sorted(nei2[i])
                nei2[i] = tuple(result)
                if nei2[i][0] < v < nei2[i][1]:
                    tc = tc + 1
    tc_doulion = round(tc * (1 / (p ** 3)))
    return tc_doulion


