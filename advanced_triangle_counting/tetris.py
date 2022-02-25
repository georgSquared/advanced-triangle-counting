import networkx as nx
from littleballoffur import HybridNodeEdgeSampler, RandomNodeEdgeSampler
from networkx import gnm_random_graph
import random
from math import factorial
import collections
import numpy as np
import time

# select random graph using gnp_random_graph() function of networkx
nodes_of_graph = 2000
# Graph = nx.gnp_random_graph(nodes_of_graph, 0.8, seed=42, directed=False)
# Graph = nx.complete_graph(nodes_of_graph)

# load the dataset using read_edgelist of networkx

Graph = nx.read_edgelist("cnr-2000.mtx", create_using=nx.Graph(), nodetype=int)

actual_e = len(Graph.edges)
# print("number of edges: ", actual_e)

true = sum(nx.triangles(Graph).values()) / 3
# print("actual triangles", true)

# set r and l. In r, we should choose normally between 0.035 and 0.045 (3.5-4.5%) of the actual graph.
r = int(0.017*actual_e)
# l usually does not need to change
l = int(0.05*r)


def probability_of_edges(graph, multiset):
    """
    Calculate the probability of sampling an edge.
    :param graph: the sampled graph
    :param multiset: R
    :return: the probability for each edge, and the total degree of the whole multiset R
    """
    r_d = 0
    for idx in multiset:
        for v in idx:
            r_d += graph.degree[v]

    prob_for_edges = []
    for idx in multiset:
        degree = []
        for v in idx:
            degree.append(graph.degree[v])
        prob_for_edges.append(min(degree) / r_d)
    return prob_for_edges, r_d


def sample_edge(prob_for_edges, graph, multiset):
    """
    Sample an edge based on the probability (that is the endpoint with minimum degree).
    :param prob_for_edges: the probability to sample an edge
    :param graph: the sampled graph
    :param multiset: R
    :return: the sampled edge
    """
    x = random.choices(multiset, weights=prob_for_edges)
    min_degree = []
    for idx in x:
        for v in idx:
            min_degree.append(graph.degree[v])

    m = min(min_degree)
    mm = max(min_degree)

    if m == mm:
        x_ = int(min(x[0]))
        y_ = int(max(x[0]))
    else:
        index_of_min = min_degree.index(m)
        index_of_max = min_degree.index(mm)
        x_ = int(x[0][index_of_min])
        y_ = int(x[0][index_of_max])
    edge = [x_, y_]

    return edge


def neighbor_query(graph, edge):
    """
    Neighbor query that takes a neighbor of the given node randomly.
    :param graph: Our sampled graph
    :param edge: the edge to take the neighbor from
    :return: the selected neighbor, or -1 to run the neighbor query again if possible neighbor is not found
    """
    try:
        return random.choice([n for n in graph.neighbors(edge[0]) if n not in edge]), 0

    except IndexError:
        return -1, -1
        # return random.choice([n for n in graph.neighbors(edge[1]) if n not in edge]), 1


def edge_count_estimator(multiset, lmix):
    """
    Edge count estimator, the second algorithm that tetris uses, in order to estimate the graph edges.
    :param multiset: the multiset R
    :param lmix: the lmix time of tetris
    :return: number of edges in the graph
    """
    Y_i = []
    # begin with Ri from index 0 and choose every other lmix-th element of multiset R
    R_i = multiset[0::lmix]
    for i in range(1, lmix):
        # save to dictionary the edges and how many times they appear in the sampling
        freq = collections.Counter(R_i)
        total_fr = sum(freq.values())
        c_i = total_fr / len(R_i)
        # compute y_i and save it
        Y_i_value = (factorial(len(R_i)) / (factorial(2) * factorial(len(R_i) - 2))) / c_i
        Y_i.append(Y_i_value)
        # continue sampling R from the next element
        R_i = multiset[i::lmix]
    sum_ = sum(Y_i)
    # print(sum_)
    Y = (1 / lmix) * sum_
    return Y


def tetris(l, r, lmix=25):
    """
    Tetris basic function that creates multiset R from sampled edges, samples an edge of this multiset and find its
    neighbors, to check if a triangle is formed between those 3 nodes.
    :param l: edges to sample from multiset R each time
    :param r: number of sample edges from the original graph (normally the length of the random walk)
    :param lmix: mixing time, fixed to 25.
    :return: estimation of triangles
    """
    # use sampler to sample edges from the graph

    # sampler = RandomNodeEdgeSampler(number_of_edges=r)
    # sampled_graph = sampler.sample(Graph)
    sampler = HybridNodeEdgeSampler(number_of_edges=r)
    sampled_graph = sampler.sample(Graph)

    R = set(sampled_graph.edges)
    R = list(R)
    # print(R)
    prob_edges, r_d = probability_of_edges(sampled_graph, R)

    Y_i = []

    for i in range(l):

        sampled_edge = sample_edge(prob_edges, sampled_graph, R)
        # neighbor of the smallest degree node
        neighbor, which = neighbor_query(sampled_graph, sampled_edge)
        if neighbor == -1 and which == -1:
            sampled_edge = sample_edge(prob_edges, sampled_graph, R)
            neighbor, which = neighbor_query(sampled_graph, sampled_edge)
        if sampled_graph.has_edge(neighbor, sampled_edge[which]):
            """
            if sampled_graph.degree[neighbor] < sampled_graph.degree[sampled_edge[which]]:
                t = False
            else:
                t = True
            """
            Y_i.append(1)
        else:
            Y_i.append(0)

    y_sum = sum(Y_i)
    Y = (1 / l) * y_sum
    # print(Y)
    m = edge_count_estimator(R, lmix)
    X = (m / r) * r_d * Y

    return X


def relative_error(predict, truth):
    mape = np.abs((truth - predict) / truth) * 100
    return mape


start = time.time()
triangles = tetris(l, r)
end = time.time()
print("error is: ", relative_error(triangles, true), "%")
print(triangles)
# count time elapsed
print(end - start)

